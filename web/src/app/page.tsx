import { RepoSearcher } from "@/app/ui/RepoSearcher";
import { RepoLoader } from "@/app/ui/RepoLoader";
import { ContentAccordion } from "@/app/ui/ContentAccordion";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col p-24">
      <RepoLoader />
      <RepoSearcher />
      <ContentAccordion />
    </main>
  );
}
