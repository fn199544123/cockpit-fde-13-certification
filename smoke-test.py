#!/usr/bin/env python3
"""在宿主机执行 python3 smoke-test.py；需 Python Playwright 和 Chromium。"""
import json, threading, functools
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
checks=[]
def ok(name): checks.append({'name':name,'status':'passed'})
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  context=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
  page=context.new_page(); errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
  assert page.locator('#rows tr').count()==12
  assert page.locator('#stats .stat').nth(2).locator('strong').inner_text()=='3'
  ok('初始台账 12 单，自动超时预警 3 单')
  page.click('#newOrder');page.fill('#orderId','WT-99990001');page.fill('#sample','YP-99990001');page.click('button[type=submit]')
  page.fill('#search','WT-99990001');assert page.locator('#rows tr').count()==1
  assert page.locator('#stats .stat').first.locator('strong').inner_text()=='1'
  page.click('[data-edit="WT-99990001"]');page.select_option('#category','性能检测');page.click('button[type=submit]')
  assert '性能检测' in page.locator('#rows').inner_text();ok('新增、修改、编号筛选与指标同步')
  page.click('[data-detail="WT-99990001"]');page.click('#advance')
  assert page.locator('.event').count()==3
  page.click('#advance');assert '请先选择' in page.locator('#detailError').inner_text()
  page.select_option('#decision','通过');page.click('#advance');page.click('#advance');page.click('#advance')
  assert '流程已完成' in page.locator('#detailContent').inner_text()
  assert page.locator('.event').count()==6
  assert page.locator('#stats .stat').nth(3).locator('strong').inner_text()=='100.0%'
  assert page.locator('#stats .stat').nth(1).locator('strong').inner_text()=='0'
  page.click('[data-close="detail"]');page.reload();page.fill('#search','WT-99990001');assert '已完成' in page.locator('#rows').inner_text()
  ok('收样→检测→报告→发证→完成，结论必填，时间线/指标/刷新持久化同步')
  page.select_option('#stageFilter','0');assert page.locator('#rows tr').count()==0
  page.select_option('#stageFilter','4');assert page.locator('#rows tr').count()==1
  with page.expect_download() as d:page.click('#export')
  csv=Path(d.value.path()).read_text(encoding='utf-8-sig');assert 'WT-99990001' in csv and 'WT-20260001' not in csv
  assert len(csv.splitlines())==2
  ok('环节组合筛选、空状态与 CSV 仅导出筛选数据')
  page.click('#clear');page.select_option('#alertFilter','late');assert page.locator('#rows tr').count()==3
  page.select_option('#resultFilter','通过');assert page.locator('#rows tr').count()==1
  ok('超时与结论交叉筛选正确')
  page.click('#clear');page.click('#newOrder');page.fill('#orderId','WT-99990001');page.click('button[type=submit]');assert '已存在' in page.locator('#formError').inner_text();page.click('[data-close="editor"]')
  page.click('#newOrder');page.fill('#orderId','WT-99990002');page.click('button[type=submit]');page.fill('#search','WT-99990002');page.click('[data-detail="WT-99990002"]');page.click('#advance');page.select_option('#decision','不通过');page.click('#advance');assert page.locator('#advance').is_disabled();page.click('[data-close="detail"]')
  assert page.locator('#stats .stat').nth(3).locator('strong').inner_text()=='0.0%'
  ok('重复委托编号拦截、不通过结论计入统计且禁止发证')
  # Freeze time to verify elapsed history and advancing boundary.
  page.click('#clear');page.clock.install();page.clock.fast_forward(3*86400000)
  page.fill('#search','WT-99990002');page.click('[data-detail="WT-99990002"]')
  assert '3.0 天' in page.locator('.stages').inner_text();page.click('[data-close="detail"]')
  ok('浏览器时钟推进 3 天后环节停留自动更新')
  page.click('#reset');page.click('[data-close="confirm"]');page.click('#clear');assert page.locator('#rows tr').count()==14
  page.click('#reset');page.click('#confirmReset');assert page.locator('#rows tr').count()==12
  page.reload();assert page.locator('#rows tr').count()==12;ok('重置取消保留数据、确认恢复且刷新保持')
  keys=page.evaluate('Object.keys(localStorage)');assert all(k.startswith('development-13-') for k in keys)
  assert not errors,errors;ok('所有存储键使用指定前缀，浏览器无脚本错误')
  page.screenshot(path=str(ROOT/'evidence-desktop.png'),full_page=True)
  page.set_viewport_size({'width':390,'height':844});page.reload();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.click('#newOrder');assert page.locator('#editor').is_visible();page.click('[data-close="editor"]')
  page.screenshot(path=str(ROOT/'evidence-mobile.png'),full_page=True);ok('390px 手机适配、弹窗可操作、页面无横向溢出')
  browser.close()
except Exception as e:
 checks.append({'name':'验收中断','status':'failed','detail':str(e)})
 raise
finally:
 server.shutdown()
 (ROOT/'smoke-test-results.json').write_text(json.dumps({'execution':'宿主机 Python Playwright / Chromium，独立浏览器上下文','tests':checks},ensure_ascii=False,indent=2))
 print(json.dumps(checks,ensure_ascii=False,indent=2))
