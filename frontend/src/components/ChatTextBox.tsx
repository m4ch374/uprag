import React, { FormEvent, useState } from "react";
import { Button } from "./ui/button";
import { SendHorizonal } from "lucide-react";
import { cn } from "@/lib/utils";
import Spinner from "./Spinner";

const ChatTextBox: React.FC<{
  className?: string;
  onTextSubmission?: (text: string, e: FormEvent<HTMLFormElement>) => void;
  loading?: boolean;
}> = ({ className, onTextSubmission, loading }) => {
  const [text, setText] = useState("");

  return (
    <form
      className={cn(
        "bg-slate-100 rounded-md border border-slate-200 focus-within:border-slate-300 transition-colors w-full",
        className,
      )}
      onSubmit={e => {
        onTextSubmission?.(text, e);
        setText("");
      }}
    >
      <textarea
        className={`resize-none w-full min-h-16 rounded-t-[inherit] p-2.5 text-lg focus:ring-0 focus:outline-none ${loading && "text-gray-500"}`}
        placeholder="Ask a question..."
        onChange={t => setText(t.target.value)}
        value={text}
        disabled={loading}
      />

      <div className="flex justify-end p-2">
        <Button
          className="bg-emerald-600 hover:bg-emerald-700 transition-colors"
          type="submit"
          disabled={loading}
        >
          {loading ? <Spinner /> : <SendHorizonal />}
        </Button>
      </div>
    </form>
  );
};

export default ChatTextBox;
