"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { atom, useAtom, useSetAtom } from "jotai";
import { ChangeEvent } from "react";
import { invoke } from "@/app/actions/invoke";
import { ContentAtom } from "./Chat";
import { useState } from "react";

const RepoAtom = atom("");

const PlaceHolder = "gitllama";

export function RepoSearcher() {
  const [repo, setRepo] = useAtom(RepoAtom);
  const setContent = useSetAtom(ContentAtom);
  const [loading, setLoading] = useState(false);

  const handleInput = (event: ChangeEvent<HTMLInputElement>) => {
    setRepo(event.target.value);
  };

  const handleSubmit = async () => {
    const str = (str: string) => {
      if (!repo) return PlaceHolder;
      return str.trim();
    };

    try {
      setLoading(true);
      const response = await invoke(str(repo));

      setContent(response);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex w-full max-w-md items-center space-x-2">
      <Input type="url" placeholder={PlaceHolder} onChange={handleInput} />
      <Button type="submit" onClick={handleSubmit} loading={loading}>
        Clone
      </Button>
    </div>
  );
}
