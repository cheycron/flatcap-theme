/* Optional Playwright runner. No dependencies installed by this file.
 * CommonJS: const run = require('./tests/browser-check'); await run(page, {url});
 * Also usable in a Playwright MCP code batch by loading this file into a module.
 */
module.exports = async function checkFlatcap(page, options = {}) {
  const url = options.url || process.env.FLATCAP_TEST_URL;
  if (!url) throw new Error('Set FLATCAP_TEST_URL or pass {url} for this repository example');
  const base = url.replace(/examples\/?(?:[?#].*)?$/, '');
  const source = await (await page.request.get(`${base}src/theme.json`)).json();
  const results = [];
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const test = async (name, fn) => {
    try { const details = await fn(); results.push({name, passed: true, details: details ?? null}); }
    catch (error) { results.push({name, passed: false, error: error.message}); }
  };
  const assert = (value, message) => { if (!value) throw new Error(message); };
  const property = name => page.evaluate(key => getComputedStyle(document.documentElement).getPropertyValue(key).trim(), name);
  const set = async (key, value) => page.locator(`#${key}`).selectOption(value);
  const hex = value => value.toUpperCase();
  const reset = async () => {
    await page.goto(url);
    await page.evaluate(() => localStorage.clear());
    await page.reload();
  };
  await reset();
  if (options.fontBaseURL) {
    // QA-only local files: never add these downloads to the actual example.
    await page.addStyleTag({content: `@font-face { font-family: 'IBM Plex Sans'; src: url('${options.fontBaseURL}/IBMPlexSans-Regular.ttf'); font-weight: 400; }
@font-face { font-family: 'IBM Plex Sans Condensed'; src: url('${options.fontBaseURL}/IBMPlexSansCondensed-Regular.ttf'); font-weight: 400; }
@font-face { font-family: 'Cascadia Code'; src: url('${options.fontBaseURL}/CascadiaCode.ttf'); font-weight: 100 900; }`});
    await test('QA font files load: Plex Sans, Condensed, Cascadia Code', async () => {
      const loaded = await page.evaluate(async () => {
        const families = ['IBM Plex Sans', 'IBM Plex Sans Condensed', 'Cascadia Code'];
        const output = [];
        for (const family of families) {
          const faces = await document.fonts.load(`400 15px "${family}"`, 'ÁÉÍÓÚ ñ Il1 O0 !==');
          output.push({family, loaded: faces.length > 0 && faces.every(face => face.status === 'loaded')});
        }
        return output;
      });
      assert(loaded.every(font => font.loaded), JSON.stringify(loaded));
      return loaded;
    });
  }
  for (const mode of ['slate', 'daylight']) {
    for (const contrast of ['standard', 'more']) {
      await test(`effective token export ${mode}/${contrast}`, async () => {
        await set('theme', mode); await set('contrast', contrast);
        const expected = {...source.themes[mode]};
        if (contrast === 'more') {
          for (const key of Object.keys(expected)) if (key.startsWith('contrast.')) expected[key.slice(9)] = expected[key];
        }
        const values = await page.evaluate(keys => {
          const css = getComputedStyle(document.documentElement);
          return Object.fromEntries(keys.map(key => [key, css.getPropertyValue('--fc-' + key.replaceAll('.', '-')).trim()]));
        }, Object.keys(expected));
        for (const [key, value] of Object.entries(expected)) assert(hex(values[key]) === value, `${key}: ${values[key]} != ${value}`);
        return {roles: Object.keys(values).length};
      });
      await test(`density independent of font ${mode}/${contrast}`, async () => {
        await set('density', 'comfortable');
        const before = await page.locator('#service-name').evaluate(el => {const s=getComputedStyle(el);return {size:s.fontSize, family:s.fontFamily, height:el.getBoundingClientRect().height};});
        await set('density', 'compact');
        const after = await page.locator('#service-name').evaluate(el => {const s=getComputedStyle(el);return {size:s.fontSize, family:s.fontFamily, height:el.getBoundingClientRect().height};});
        assert(before.size === after.size && before.family === after.family && after.height < before.height, JSON.stringify({before, after}));
        return {before, after};
      });
      for (const density of ['comfortable', 'compact']) {
        await set('density', density);
        for (const width of [320, 375, 768, 1280]) {
          await test(`reflow ${width}px ${mode}/${contrast}/${density}`, async () => {
            await page.setViewportSize({width, height: 960});
            const sizes = await page.evaluate(() => ({viewport: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth}));
            assert(sizes.scroll <= sizes.viewport + 1, JSON.stringify(sizes));
            return sizes;
          });
        }
      }
    }
  }
  await test('Condensed is opt-in and independent of density', async () => {
    await page.locator('#condensed').check();
    const family = await page.locator('.dense-label').first().evaluate(el => getComputedStyle(el).fontFamily);
    assert(family.startsWith('"IBM Plex Sans Condensed"'), family);
    await set('density', 'comfortable');
    assert(await page.locator('#condensed').isChecked(), 'Density changed Condensed preference');
    await page.locator('#condensed').uncheck();
  });
  await test('system light + more and manual override precedence', async () => {
    await page.emulateMedia({colorScheme:'light', contrast:'more'});
    await set('theme', 'system'); await set('contrast', 'system');
    assert(hex(await property('--fc-bg-canvas')) === source.themes.daylight['bg.canvas'], 'System light not effective');
    assert(hex(await property('--fc-text-primary')) === source.themes.daylight['contrast.text.primary'], 'System contrast not effective');
    await set('theme', 'slate'); await set('contrast', 'standard');
    assert(hex(await property('--fc-bg-canvas')) === source.themes.slate['bg.canvas'], 'Manual mode not honored');
    assert(hex(await property('--fc-text-primary')) === source.themes.slate['text.primary'], 'Manual standard not honored');
  });
  await test('system dark + no-preference', async () => {
    await page.emulateMedia({colorScheme:'dark', contrast:'no-preference'});
    await set('theme', 'system'); await set('contrast', 'system');
    assert(hex(await property('--fc-bg-canvas')) === source.themes.slate['bg.canvas'], 'System dark not effective');
    assert(hex(await property('--fc-text-primary')) === source.themes.slate['text.primary'], 'Standard contrast not effective');
  });
  await test('literal ligatures disabled', async () => {
    const value = await page.locator('.literal').evaluate(el => {const css=getComputedStyle(el);return {ligatures:css.fontVariantLigatures,features:css.fontFeatureSettings};});
    assert(value.ligatures === 'none' && value.features.includes('"calt" 0'), JSON.stringify(value));
    return value;
  });
  await test('invalid name is associated, persistent and focused', async () => {
    await page.locator('#service-name').fill('   '); await page.locator('#save').click();
    assert(await page.locator('#name-error').isVisible(), 'Missing error');
    assert(await page.locator('#service-name').getAttribute('aria-invalid') === 'true', 'Missing invalid state');
    assert(await page.locator('#service-name').evaluate(el => el === document.activeElement), 'Invalid field not focused');
    await page.locator('#environment').focus();
    assert(await page.locator('#name-error').isVisible(), 'Error vanished on blur');
  });
  await test('successful save persists text, avoids injection and preserves focus', async () => {
    await page.locator('#service-name').fill('<script>not markup</script>');
    await page.locator('#save').focus(); await page.keyboard.press('Enter');
    const text = await page.locator('#form-status').textContent();
    assert(text.includes('<script>not markup</script>'), text);
    assert(await page.locator('#form-status script').count() === 0, 'HTML injected');
    assert(await page.locator('#save').evaluate(el => el === document.activeElement), 'Save moved focus');
    assert(await page.locator('#name-error').isHidden(), 'Old error remains');
  });
  await test('readonly is focusable, disabled action is not', async () => {
    assert(await page.locator('#environment').getAttribute('readonly') !== null, 'Readonly contract');
    assert(await page.getByRole('button', {name:'Publish',exact:true}).isDisabled(), 'Publish enabled');
    await page.locator('#environment').focus(); await page.keyboard.press('Tab');
    assert(await page.locator('#save').evaluate(el => el === document.activeElement), 'Unexpected tab order');
    await page.keyboard.press('Tab');
    assert(!(await page.getByRole('button',{name:'Publish',exact:true}).evaluate(el => el === document.activeElement)), 'Disabled in tab sequence');
  });
  await test('200% root text and WCAG text spacing: no page overflow', async () => {
    await page.setViewportSize({width:1280,height:960});
    const style = await page.addStyleTag({content:'html { font-size: 200% !important; } * { line-height:1.5 !important; letter-spacing:.12em !important; word-spacing:.16em !important; } p { margin-bottom:2em !important; }'});
    const sizes = await page.evaluate(() => ({viewport:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}));
    assert(sizes.scroll <= sizes.viewport + 1, JSON.stringify(sizes));
    assert(await page.locator('#save').isVisible(), 'Save hidden');
    await style.evaluate(el => el.remove());
    return sizes;
  });
  await test('reduced motion token', async () => {
    await page.emulateMedia({reducedMotion:'reduce'});
    assert(await property('--fc-motion-fast') === '0ms', 'Reduced motion not applied');
    await page.emulateMedia({reducedMotion:'no-preference'});
  });
  await test('forced colors retains borders and keyboard focus', async () => {
    await page.emulateMedia({forcedColors:'active'});
    await page.locator('#save').focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab');
    const css = await page.locator('#save').evaluate(el => {const s=getComputedStyle(el);return {border:s.borderTopStyle,outline:s.outlineStyle,width:s.outlineWidth,focused:el.matches(':focus-visible')};});
    assert(css.border === 'solid' && css.outline !== 'none' && css.width === '2px' && css.focused, JSON.stringify(css));
    await page.emulateMedia({forcedColors:'none'});
    return css;
  });
  await test('preference restore after reload', async () => {
    await set('theme','daylight'); await set('contrast','more'); await set('density','compact');
    await page.locator('#condensed').check(); await page.reload();
    for (const [id, value] of [['theme','daylight'],['contrast','more'],['density','compact']]) assert(await page.locator(`#${id}`).inputValue() === value, id);
    assert(await page.locator('#condensed').isChecked(), 'Condensed not restored');
  });
  await test('keyboard skip link and visible focus', async () => {
    await page.reload(); await page.keyboard.press('Tab');
    const visible = await page.locator('.skip').evaluate(el => {const r=el.getBoundingClientRect();return el === document.activeElement && r.top >= 0;});
    assert(visible, 'Skip link not first/visible');
    await page.keyboard.press('Enter');
    assert(await page.locator('#content').evaluate(el => el === document.activeElement), 'Skip target not focused');
  });
  await test('no-JavaScript baseline', async () => {
    const context = await page.context().browser().newContext({javaScriptEnabled:false, viewport:{width:320,height:900}});
    try {
      const other = await context.newPage(); await other.goto(url);
      assert(await other.locator('#preferences').evaluate(el => el.disabled) && await other.locator('#theme').isDisabled(), 'Unavailable JS controls enabled');
      const sizes = await other.evaluate(() => ({viewport:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}));
      assert(sizes.scroll <= sizes.viewport + 1, JSON.stringify(sizes));
      assert(await other.locator('h1').isVisible(), 'Content hidden without JS');
      assert(await other.locator('#save').isDisabled(), 'Form could submit without its local-only JS handler');
      return sizes;
    } finally { await context.close(); }
  });
  await test('invalid stored preferences fall back safely', async () => {
    await page.evaluate(() => localStorage.setItem('flatcap-example', '{broken-json')); await page.reload();
    assert(await page.locator('#theme').inputValue() === 'slate', 'Malformed storage altered default');
    await page.evaluate(() => localStorage.setItem('flatcap-example', JSON.stringify({theme:'unexpected', density:'tiny'}))); await page.reload();
    assert(await page.locator('#theme').inputValue() === 'slate' && await page.locator('#density').inputValue() === 'comfortable', 'Unknown values accepted');
  });
  await test('JavaScript runtime errors', () => { assert(errors.length === 0, errors.join('\n')); });
  const report = {version:source.version, browser:page.context().browser().version(), scope:'Repository example in Chromium; media emulation, not physical hardware/AT/user testing', fonts:options.fontBaseURL ? 'QA-only supplied font files; see hash manifest' : 'Local host fonts or fallbacks, exact families not asserted', total:results.length, passed:results.filter(r=>r.passed).length, results};
  if (report.passed !== report.total) {
    const error = new Error(JSON.stringify(report)); error.report=report; throw error;
  }
  return report;
};
