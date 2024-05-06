"use client";
import { useEffect, useState } from "react";
import { remark } from "remark";
import html from "remark-html";

// 将Markdown转换为HTML
const convertMarkdownToHtml = async (markdownText: string) => {
  const processedContent = await remark().use(html).process(markdownText);

  const htmlContent = processedContent.toString();

  return htmlContent;
};

const MarkdownToHtml = ({ markdownText }: { markdownText: string }) => {
  const [html, setHtml] = useState("");

  useEffect(() => {
    convertMarkdownToHtml(markdownText)
      .then((html) => {
        setHtml(html);
      })
      .catch(() => {
        setHtml(markdownText);
      });
  }, [markdownText]);

  return <div className="w-full" dangerouslySetInnerHTML={{ __html: html }} />;
};

export default MarkdownToHtml;
