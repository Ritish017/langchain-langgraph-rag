# 🎨 Mermaid Diagram - View Your RAG Workflow

## ✅ Files Generated

1. **`rag_workflow.mermaid`** - Raw Mermaid code
2. **`RAG_WORKFLOW_DIAGRAM.md`** - Markdown file with embedded diagram

## 🌐 View Online (Easiest Way)

### Method 1: Mermaid Live Editor (Recommended)

1. Open: **https://mermaid.live**
2. Copy the content from `rag_workflow.mermaid`
3. Paste into the editor
4. **✨ Instant beautiful diagram!**
5. Export as PNG/SVG using the "Actions" menu

### Method 2: VS Code Preview

1. Install extension: **"Markdown Preview Mermaid Support"**
   - Press `Ctrl+Shift+X`
   - Search: "Mermaid"
   - Install the one by Matt Bierner
2. Open `RAG_WORKFLOW_DIAGRAM.md`
3. Press `Ctrl+Shift+V` to preview
4. **✨ See the diagram right in VS Code!**

### Method 3: GitHub (If you have a repo)

1. Push `RAG_WORKFLOW_DIAGRAM.md` to GitHub
2. Open it on GitHub
3. **✨ GitHub auto-renders Mermaid diagrams!**

## 📊 What You'll See

The diagram shows:

```
┌─────────┐
│  START  │
└────┬────┘
     │
     ▼
┌────────────────────────┐
│generate_query_or_respond│ (LLM Router)
└─────┬──────────────────┘
      │
   ┌──┴──┐
   │     │
   ▼     ▼
 END   retrieve (Vector Store)
         │
         ▼
   grade_documents (Quality Check)
         │
      ┌──┴──┐
      │     │
      ▼     ▼
 generate  rewrite
 _answer   _question
    │         │
    ▼         └──> (loops back)
   END
```

**With proper styling:**
- Rounded boxes for START/END
- Different colors for different node types
- Dashed lines for conditional edges
- Solid lines for direct edges
- Labels on edges (like "tools")

## 🎨 Styling Features

The generated Mermaid diagram includes:
- ✅ Purple theme (`fill:#f2f0ff`)
- ✅ Highlighted end node (`fill:#bfb6fc`)
- ✅ Transparent start node
- ✅ Clean linear flow
- ✅ Conditional routing visualization

## 💡 Pro Tips

### Customize Colors
Edit `rag_workflow.mermaid` and change:
```mermaid
classDef default fill:#f2f0ff,line-height:1.2
```

### Export High-Quality PNG
From mermaid.live:
1. Click "Actions" menu
2. Choose "PNG" or "SVG"
3. Select resolution (2x, 3x for high-res)
4. Download

### Use in Documentation
Copy the mermaid code block into any markdown file:
````markdown
```mermaid
[paste mermaid code here]
```
````

## 🔧 Advanced: Install Mermaid CLI (Optional)

If you want to generate PNGs locally:

```powershell
# Install Node.js first (from nodejs.org)
npm install -g @mermaid-js/mermaid-cli

# Generate PNG
mmdc -i rag_workflow.mermaid -o rag_workflow_diagram.png

# Generate SVG
mmdc -i rag_workflow.mermaid -o rag_workflow_diagram.svg -t neutral
```

## 📸 Example Output

Your diagram will show:
- **Green/Blue nodes** - Processing steps
- **Purple endpoint** - Final output
- **Dashed arrows** - Conditional paths
- **Solid arrows** - Direct flow
- **Edge labels** - Decision criteria ("tools", etc.)

## 🚀 Quick Start

**The fastest way to see your diagram RIGHT NOW:**

1. Copy this link: **https://mermaid.live**
2. Open it in your browser
3. Paste the content from `rag_workflow.mermaid`
4. **Done!** 🎉

Enjoy your beautiful workflow diagram! ✨
