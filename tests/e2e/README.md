
# E2E (manual)
1) Start API: `pwsh -File C:\Agent\bin\agent.ps1 start`
2) Put `todo.md` into one of your sandboxes and run `python C:\Agent\bin\reindex.py`
3) Press `Ctrl+Space` and say: *"Summarize the key tasks from 'C:\Users\<YOU>\Projects\todo.md' and cite the file."*
4) Expected: Spoken bullet summary; `/tools/fs` read occurs; `audit\YYYY-MM-DD.jsonl` contains entries for stt, fs, chat, tts.
