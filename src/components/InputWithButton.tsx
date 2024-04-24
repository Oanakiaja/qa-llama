import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function InputWithButton() {
  return (
    <div className="flex w-full max-w-md items-center space-x-2">
      <Input type="url" placeholder="https://github.com/oanakiaja/gitllama" />
      <Button type="submit">Clone</Button>
    </div>
  )
}