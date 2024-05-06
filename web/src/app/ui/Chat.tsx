"use client";
import MarkdownToHtml from "@/components/MarkdownToHtml";
import { useAtomValue } from "jotai";
import { atomWithStorage } from "jotai/utils";

export const ContentAtom = atomWithStorage(
  "chat-content",
  "",
  window.localStorage as any,
  {
    getOnInit: true,
  }
);

// function textToHtml(text: string) {
//   const paragraphs = text.split("\\n\\n");

//   return paragraphs
//     .map((paragraphText) => {
//       paragraphText = paragraphText.replace(/\\\"/g, "&quot;");
//       paragraphText = paragraphText.replace(/\n/g, "<br />");

//       return `<p>${paragraphText}</p>`;
//     })
//     .join("<br />");
// }

const Chat = () => {
  const content = useAtomValue(ContentAtom) || "";

  return (
    <div className="flex-1 mt-12 ">
      <MarkdownToHtml markdownText={content} />
    </div>
  );
};

export default Chat;
