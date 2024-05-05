import { clientFetchApi, FetchOptions } from "./fetch";

export const streaming_qa = (
  params: {
    session: string;
    question: string;
  },
  options?: FetchOptions
): Promise<undefined> => clientFetchApi("qa", "POST", "sse")(params, options);
