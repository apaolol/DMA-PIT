import json
import sys
from pathlib import Path
from jupyter_client import KernelManager

root = Path(__file__).resolve().parents[1]
path = root / 'DMA.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
km = KernelManager(kernel_name='python3')
km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
km.start_kernel(cwd=str(root))
client = km.blocking_client()
client.start_channels()
failures = []
try:
    client.wait_for_ready(timeout=30)
    for index, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        cell['outputs'] = []
        message_id = client.execute(cell['source'], stop_on_error=True)
        while True:
            msg = client.get_iopub_msg(timeout=60)
            if msg.get('parent_header', {}).get('msg_id') != message_id:
                continue
            kind = msg['header']['msg_type']
            content = msg['content']
            if kind == 'execute_input':
                cell['execution_count'] = content['execution_count']
            elif kind == 'stream':
                cell['outputs'].append({'output_type': 'stream', 'name': content['name'], 'text': content['text']})
            elif kind in ('execute_result', 'display_data'):
                out = {'output_type': kind, 'data': content['data'], 'metadata': content.get('metadata', {})}
                if kind == 'execute_result':
                    out['execution_count'] = content['execution_count']
                cell['outputs'].append(out)
            elif kind == 'error':
                cell['outputs'].append({'output_type': 'error', 'ename': content['ename'], 'evalue': content['evalue'], 'traceback': content['traceback']})
                failures.append((index, content['ename'], content['evalue']))
            elif kind == 'status' and content['execution_state'] == 'idle':
                break
        print('Executed cell', index, 'outputs', len(cell['outputs']))
        if failures:
            break
finally:
    client.stop_channels()
    km.shutdown_kernel(now=True)
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
if failures:
    raise RuntimeError(failures)
print('All notebook code cells executed successfully.')
