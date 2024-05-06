"use client";
import { atom, useAtomValue } from "jotai";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export const ReferencesAtom = atom<{ source: string; content: string }[]>([]);

const References = () => {
  const references = useAtomValue(ReferencesAtom) || [];

  return (
    <div className="flex">
      {references.map((reference, idx) => (
        <Card key={idx}>
          <CardHeader>
            <CardTitle>
              <a href={reference.source}>{reference.source}</a>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p>{reference.content}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default References;
