"use server";

export async function invoke(str: string) {
  const url = `${process.env.BACKEND_URL}/invoke/${str}`
  console.log(url)

  const response = await fetch(url);
  
  if (!response.ok) {
    return "[error]: python server";
  }

  return response.text();
}
