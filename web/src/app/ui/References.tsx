"use client";
import { atom, useAtomValue } from "jotai";
import { Button } from "@/components/ui/button";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { atomWithStorage } from "jotai/utils";

export const ReferencesAtom = atomWithStorage<
  { source: string; content: string }[]
>("references", []);

const References = () => {
  const references = useAtomValue(ReferencesAtom) || [];

  return (
    <div className="flex w-full flex-wrap">
      {references?.map?.((reference, idx) => (
        <HoverCard key={idx}>
          <HoverCardTrigger asChild>
            <Button variant="link">
              <a href={reference.source}>{reference.source}</a>
            </Button>
          </HoverCardTrigger>
          <HoverCardContent className="w-80">
            <div className="flex justify-between space-x-4">
              <div className="space-y-1">
                <h4 className="text-sm font-semibold">{reference.source}</h4>
                <p className="text-sm">{reference.content}</p>
                <div className="flex items-center pt-2">
                  <span className="text-xs text-muted-foreground">
                    TODO: meta info
                  </span>
                </div>
              </div>
            </div>
          </HoverCardContent>
        </HoverCard>
      ))}
    </div>
  );
};

export default References;
