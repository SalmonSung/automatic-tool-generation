# Guide: How to use cli tool  
>[!Warning]
>Currently cli tool doesn't support configuration. Check [RoadMap](some.link)
1. **Start Analysis**  
   Run the following command to generate tools based on your input file:
   ```bash
   python atg_cli.py generate --path <path to the file>
   ```
2. **Find the result**  
   Replay the most recent result to view the output path or contents:
   ```bash
   python atg_cli.py replay
   python atg_cli.py replay --mode path
   python atg_cli.py replay --mode content
   ```
