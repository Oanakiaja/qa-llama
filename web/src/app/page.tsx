import { RepoSearcher } from "@/app/ui/RepoSearcher";
import Chat from "@/app/ui/Chat";
import { RepoLoader } from "./ui/RepoLoader";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <RepoLoader />
      <RepoSearcher />
      <Chat />
    </main>
  );
}
