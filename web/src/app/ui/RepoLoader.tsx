"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { atom, useAtom } from "jotai";
import { ChangeEvent } from "react";
import { useState } from "react";
import { loadDoc } from "../actions/server/agent";

const RepoAtom = atom("");

const PlaceHolder = "https://lilianweng.github.io/posts/2023-06-23-agent";

export function RepoLoader() {
  const [repo, setRepo] = useAtom(RepoAtom);
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
      await loadDoc({ repo: str(repo) });

      console.log("[repo]: str(repo) loaded into vector databases.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex w-full  max-w-xl items-center space-x-2 my-4 self-center">
      <Input type="url" placeholder={PlaceHolder} onChange={handleInput} />
      <Button type="submit" onClick={handleSubmit} loading={loading}>
        Load ~
      </Button>
    </div>
  );
}
