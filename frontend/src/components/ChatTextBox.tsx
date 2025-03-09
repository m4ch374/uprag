import React from "react";
import { Button } from "./ui/button";
import { SendHorizonal } from "lucide-react";
import { cn } from "@/lib/utils";

const ChatTextBox: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div
      className={cn(
        "bg-slate-100 rounded-md border border-slate-200 focus-within:border-slate-300 transition-colors w-full",
        className,
      )}
    >
      <textarea
        className="resize-none w-full min-h-16 rounded-t-[inherit] p-2.5 text-lg focus:ring-0 focus:outline-none"
        placeholder="Ask a question..."
      />

      <div className="flex justify-end p-2">
        <Button className="bg-emerald-600 hover:bg-emerald-700 transition-colors">
          <SendHorizonal />
        </Button>
      </div>
    </div>
  );
};

export default ChatTextBox;
