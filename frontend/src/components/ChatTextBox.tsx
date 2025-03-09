import React, { FormEvent, useState } from "react";
import { Button } from "./ui/button";
import { SendHorizonal } from "lucide-react";
import { cn } from "@/lib/utils";
import Spinner from "./Spinner";
import DocumentSelector from "./DocumentSelector";
import { TKnowledge } from "@/lib/types/services/knowledge.servies";

const ChatTextBox: React.FC<{
  className?: string;
  onTextSubmission?: (
    text: string,
    knowledges: TKnowledge[],
    e: FormEvent<HTMLFormElement>,
  ) => void;
  loading?: boolean;
  defaultKnowledge?: TKnowledge[];
}> = ({ className, onTextSubmission, loading, defaultKnowledge }) => {
  const [text, setText] = useState("");
  const documentController = useState<TKnowledge[]>(defaultKnowledge || []);

  return (
    <form
      className={cn(
        "bg-slate-100 rounded-md border border-slate-200 focus-within:border-slate-300 transition-colors w-full",
        className,
      )}
      onSubmit={e => {
        onTextSubmission?.(text, documentController[0], e);
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

      <div className="flex justify-between p-2">
        <DocumentSelector documentController={documentController} />

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
