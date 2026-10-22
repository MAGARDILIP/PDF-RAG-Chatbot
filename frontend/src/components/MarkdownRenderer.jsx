import React from "react";

// Helper to parse inline styles like **bold**, *italic*, and `code`
function renderInline(text) {
  if (!text) return "";

  // Split by markdown inline syntax
  const parts = [];
  let remaining = text;
  let key = 0;

  while (remaining.length > 0) {
    // Bold: **text**
    const boldMatch = remaining.match(/^(.*?)\*\*(.+?)\*\*(.*)$/s);
    // Italic: *text* (when not preceded by *)
    const italicMatch = remaining.match(/^(.*?)\*([^*]+?)\*(.*)$/s);
    // Inline code: `text`
    const codeMatch = remaining.match(/^(.*?)`([^`]+?)`(.*)$/s);

    // Find the earliest match
    const matches = [
      boldMatch ? { type: "bold", index: boldMatch[1].length, full: boldMatch } : null,
      italicMatch ? { type: "italic", index: italicMatch[1].length, full: italicMatch } : null,
      codeMatch ? { type: "code", index: codeMatch[1].length, full: codeMatch } : null,
    ].filter(Boolean).sort((a, b) => a.index - b.index);

    if (matches.length === 0) {
      parts.push(remaining);
      break;
    }

    const first = matches[0];
    const before = first.full[1];
    const content = first.full[2];
    const after = first.full[3];

    if (before) {
      parts.push(before);
    }

    if (first.type === "bold") {
      parts.push(
        <strong key={key++} className="font-semibold text-gray-900">
          {renderInline(content)}
        </strong>
      );
    } else if (first.type === "italic") {
      parts.push(
        <em key={key++} className="italic text-gray-600">
          {content}
        </em>
      );
    } else if (first.type === "code") {
      parts.push(
        <code key={key++} className="bg-gray-100 text-primary-700 px-1 py-0.5 rounded text-xs font-mono">
          {content}
        </code>
      );
    }

    remaining = after;
  }

  return parts;
}

// Full Markdown block renderer (supports Headings, Tables, Lists, Paragraphs)
function MarkdownRenderer({ content, isUser = false }) {
  if (!content) return null;

  if (isUser) {
    return <span className="whitespace-pre-wrap">{content}</span>;
  }

  const lines = content.split("\n");
  const blocks = [];
  let i = 0;
  let blockKey = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Skip empty lines
    if (!trimmed) {
      i++;
      continue;
    }

    // 1. Table Detection (starts and ends with |)
    if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
      const tableLines = [];
      while (i < lines.length && lines[i].trim().startsWith("|") && lines[i].trim().endsWith("|")) {
        tableLines.push(lines[i].trim());
        i++;
      }

      if (tableLines.length >= 2) {
        // Parse rows
        const parseRow = (rowStr) =>
          rowStr
            .slice(1, -1)
            .split("|")
            .map((cell) => cell.trim());

        const headers = parseRow(tableLines[0]);
        // Filter out separator lines like |---|---|
        const bodyRows = tableLines.slice(1).filter((r) => !/^\|[\s\-:|]+\|$/.test(r)).map(parseRow);

        blocks.push(
          <div key={blockKey++} className="my-3 overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
            <table className="w-full text-xs text-left border-collapse bg-white">
              <thead className="bg-primary-50 text-primary-900 font-semibold border-b border-gray-200">
                <tr>
                  {headers.map((h, hi) => (
                    <th key={hi} className="px-3 py-2 border-r last:border-r-0 border-gray-200">
                      {renderInline(h)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {bodyRows.map((row, ri) => (
                  <tr key={ri} className={ri % 2 === 0 ? "bg-white hover:bg-gray-50" : "bg-gray-50/50 hover:bg-gray-100/50"}>
                    {row.map((cell, ci) => (
                      <td key={ci} className="px-3 py-2 border-r last:border-r-0 border-gray-200 text-gray-700 align-top">
                        {renderInline(cell)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        continue;
      }
    }

    // 2. Headings (# Header, ## Header, ### Header)
    const headerMatch = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (headerMatch) {
      const level = headerMatch[1].length;
      const title = headerMatch[2];
      if (level === 1 || level === 2) {
        blocks.push(
          <h3 key={blockKey++} className="text-sm font-bold text-gray-900 mt-3 mb-1 border-b border-gray-100 pb-1">
            {renderInline(title)}
          </h3>
        );
      } else {
        blocks.push(
          <h4 key={blockKey++} className="text-xs font-semibold text-gray-800 mt-2 mb-1">
            {renderInline(title)}
          </h4>
        );
      }
      i++;
      continue;
    }

    // 3. Bullet points (- item or * item)
    if (/^[-*]\s+/.test(trimmed)) {
      const listItems = [];
      while (i < lines.length && /^[-*]\s+/.test(lines[i].trim())) {
        listItems.push(lines[i].trim().replace(/^[-*]\s+/, ""));
        i++;
      }

      blocks.push(
        <ul key={blockKey++} className="my-2 space-y-1 pl-4 list-disc list-outside text-gray-700 text-xs">
          {listItems.map((item, li) => (
            <li key={li}>{renderInline(item)}</li>
          ))}
        </ul>
      );
      continue;
    }

    // 4. Numbered list (1. item)
    if (/^\d+\.\s+/.test(trimmed)) {
      const listItems = [];
      while (i < lines.length && /^\d+\.\s+/.test(lines[i].trim())) {
        listItems.push(lines[i].trim().replace(/^\d+\.\s+/, ""));
        i++;
      }

      blocks.push(
        <ol key={blockKey++} className="my-2 space-y-1 pl-4 list-decimal list-outside text-gray-700 text-xs">
          {listItems.map((item, li) => (
            <li key={li}>{renderInline(item)}</li>
          ))}
        </ol>
      );
      continue;
    }

    // 5. Normal paragraph
    blocks.push(
      <p key={blockKey++} className="mt-1.5 first:mt-0 text-gray-800 leading-relaxed text-xs sm:text-sm">
        {renderInline(trimmed)}
      </p>
    );
    i++;
  }

  return <div className="space-y-1">{blocks}</div>;
}

export default MarkdownRenderer;
