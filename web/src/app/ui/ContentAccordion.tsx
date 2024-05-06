"use client";
import Chat, { ContentAtom } from "@/app/ui/Chat";
import References, { ReferencesAtom } from "@/app/ui/References";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { getDefaultStore, useAtom, useAtomValue } from "jotai";
import { atomWithDefault } from "jotai/utils";

export const ComputedKeysAtom = atomWithDefault((get) => {
  let keys = [];
  const refs = get(ReferencesAtom);
  const content = get(ContentAtom) as any;

  if (refs?.length) keys.push("References");
  if (content?.length) keys.push("Content");
  return keys;
});

const setComputedKeys = (fn: (prev: string[]) => string[]) =>
  getDefaultStore().set(ComputedKeysAtom, fn);

export const toggleComputedKeys = (key: string, forceValue?: boolean) => {
  const computedKeys = getDefaultStore().get(ComputedKeysAtom);
  if (computedKeys.includes(key)) {
    if (forceValue === true) return;
    setComputedKeys((prev: string[]) => prev.filter((k) => k !== key));
  } else {
    if (forceValue === false) return;
    setComputedKeys((prev: string[]) => [...prev, key]);
  }
};

export const ContentAccordion = () => {
  const computedKeys = useAtomValue(ComputedKeysAtom);

  const triggerItem = (key: string) => () => toggleComputedKeys(key);

  return (
    <Accordion type="multiple" value={computedKeys}>
      <AccordionItem value="References" onClick={triggerItem("References")}>
        <AccordionTrigger>References</AccordionTrigger>
        <AccordionContent>
          <References />
        </AccordionContent>
      </AccordionItem>
      <AccordionItem value="Content" onClick={triggerItem("Content")}>
        <AccordionTrigger>Content</AccordionTrigger>
        <AccordionContent>
          <Chat />
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
};
