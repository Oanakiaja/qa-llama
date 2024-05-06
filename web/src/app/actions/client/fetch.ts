const HTTP_WAY_MAP = {
  http: "stream",
  sse: "astream",
} as const;

const END_POINT = "http://127.0.0.1:8000";

type HTTP_WAY = keyof typeof HTTP_WAY_MAP;

let controller: AbortController | undefined;
const createSignal = () => {
  controller = new AbortController();
  return controller.signal;
};

export const abortSignal = () => {
  try {
    controller?.abort?.();
  } catch (e) {
    console.log("abort signal error:", e);
  }
};

export type FetchOptions = {
  setLoading?: (loading: boolean) => void;
  handleSSECallback?: (type: string, content: string) => void;
};

export const clientFetchApi =
  (path: string, method: "GET" | "POST" = "POST", async: HTTP_WAY) =>
  async <Params extends Record<string, unknown>, Resp = void>(
    body: Params,
    options?: FetchOptions
  ) => {
    let url = `${END_POINT}/${
      HTTP_WAY_MAP[async as keyof typeof HTTP_WAY_MAP]
    }/${path}`;
    if (method === "GET") {
      url += `?${new URLSearchParams(JSON.stringify(body))}`;
    }

    const { handleSSECallback, setLoading } = options || {};

    setLoading?.(true);
    const response = await fetch(url, {
      method,
      body: method === "POST" ? JSON.stringify(body) : undefined,
      headers: {
        "Content-Type": "application/json",
      },
      signal: createSignal(),
    });

    if (!response.ok) {
      throw "[error]: python server!";
    }

    //  async === http once
    if (async === "http") {
      try {
        const json = (await response.json()) as Resp;
        return json;
      } finally {
        setLoading?.(false);
      }
    }

    // async === 'sse'
    if (async !== "sse") {
      throw "[error]: Not support fetch way!";
    }

    if (!response.body) {
      throw "[error]: python server!";
    }
    try {
      await handleSSE(response, handleSSECallback);
    } finally {
      setLoading?.(false);
    }
  };

const handleSSE = async (
  response: Response,
  handler?: (type: string, content: string) => void | undefined
) => {
  const reader = response!.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }
    const str = decoder.decode(value);
    try {
      const [type, content] = parseSSEEvent(str);
      handler?.(type, content);
    } catch (error) {
      console.error("Error parsing message:", error);
    }
  }
};

const parseSSEEvent = (str: string) => {
  const [_, type, content] = str.match(/^event:(.*)\ndata:(.*)\n\n$/s) || [];
  return [type, content];
};
