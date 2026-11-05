/* Optional Playwright capture helper. No dependencies installed by this file.
 * module.exports(page, {url, fontBaseURL?, save: async (name, pngBuffer) => ...})
 * The caller owns output files and browser lifetime. See images/readme/README.md.
 */
module.exports = async function captureVisuals(page, options = {}) {
  const url = options.url;
  if (!url || typeof options.save !== 'function') throw new Error('Pass repository root {url, save}');
  const base = url.replace(/\/$/, '');
  const fontBase = options.fontBaseURL?.replace(/\/$/, '');
  const captures = [];
  const fontNames = ['IBM Plex Sans', 'IBM Plex Sans Condensed', 'Cascadia Code'];
  const fonts = async () => {
    if (!fontBase) return 'Local fonts or fallbacks; exact families not asserted';
    if (!/^https?:\/\/[^'"\s]+$/.test(fontBase)) throw new Error('Invalid fixture URL');
    await page.addStyleTag({content: `
      @font-face { font-family:'IBM Plex Sans'; src:url('${fontBase}/IBMPlexSans-Regular.ttf'); font-weight:400; }
      @font-face { font-family:'IBM Plex Sans Condensed'; src:url('${fontBase}/IBMPlexSansCondensed-Regular.ttf'); font-weight:400; }
      @font-face { font-family:'Cascadia Code'; src:url('${fontBase}/CascadiaCode.ttf'); font-weight:100 900; }
    `});
    const loaded = await page.evaluate(async families => {
      const output = [];
      for (const family of families) {
        const faces = await document.fonts.load(`400 15px "${family}"`, 'Á ñ Il1 O0 !==');
        output.push({family, loaded:faces.length > 0 && faces.every(face => face.status === 'loaded')});
      }
      await document.fonts.ready;
      return output;
    }, fontNames);
    if (loaded.some(font => !font.loaded)) throw new Error('Fixture font failed to load');
    return loaded;
  };
  await page.emulateMedia({colorScheme:'dark', contrast:'no-preference', forcedColors:'none', reducedMotion:'no-preference'});
  await page.setViewportSize({width:1440, height:1100});
  await page.goto(`${base}/docs/visual-preview.html`);
  const boardFonts = await fonts();
  for (const name of ['overview', 'palette']) {
    const target = page.locator(`#${name}`);
    const bounds = await target.boundingBox();
    const png = await target.screenshot({type:'png'});
    await options.save(name, png);
    captures.push({name, kind:'illustrative board', bounds, fonts:boardFonts, bytes:png.length});
  }
  for (const [name, theme, width] of [
    ['example-slate', 'slate', 1280], ['example-daylight', 'daylight', 1280], ['example-mobile', 'slate', 375]
  ]) {
    await page.setViewportSize({width, height:960});
    await page.goto(`${base}/examples/`);
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    await page.locator('#theme').selectOption(theme);
    await page.locator('#contrast').selectOption('standard');
    await page.locator('#density').selectOption('comfortable');
    const loaded = await fonts();
    // Don't present the select's transient focus ring as an intentional example state.
    await page.locator('#density').evaluate(el => el.blur());
    const dimensions = await page.evaluate(() => ({viewport:innerWidth, clientWidth:document.documentElement.clientWidth,
      scrollWidth:document.documentElement.scrollWidth, height:document.documentElement.scrollHeight}));
    if (dimensions.scrollWidth > dimensions.clientWidth) throw new Error(`${name}: horizontal page overflow`);
    const png = await page.screenshot({fullPage:true, type:'png'});
    await options.save(name, png);
    captures.push({name, kind:'repository example', theme, contrast:'standard', density:'comfortable', dimensions, fonts:loaded, bytes:png.length});
  }
  return {version:'2.0.0', browser:page.context().browser().version(), captures};
};
