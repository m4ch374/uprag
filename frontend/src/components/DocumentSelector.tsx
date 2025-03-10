import React, { Dispatch, SetStateAction, useMemo, useState } from "react";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import { Button } from "./ui/button";
import { FilePlus, X } from "lucide-react";
import useToken from "@/lib/hooks/useToken.hooks";
import { useListKnowledge } from "@/lib/services/knowledge.service";
import { TKnowledge } from "@/lib/types/services/knowledge.servies";

const DocumentSelector: React.FC<{
  documentController: [TKnowledge[], Dispatch<SetStateAction<TKnowledge[]>>];
}> = ({ documentController }) => {
  const [open, setOpen] = useState(false);

  const accessToken = useToken();
  const { data: knowledges } = useListKnowledge(accessToken);

  const [selectedKnowledge, setSelectedKnowledge] = documentController;

  const filteredKnowledge = useMemo(
    () =>
      knowledges?.knowledges.filter(
        k => !selectedKnowledge.find(s => k.id === s.id),
      ),
    [knowledges, selectedKnowledge],
  );

  return (
    <div className="flex gap-2 items-center flex-wrap">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger>
          <FilePlus className="mt-0.5 size-6 stroke-neutral-500 cursor-pointer" />
        </PopoverTrigger>
        <PopoverContent className="bg-slate-100 w-auto min-w-48 p-2">
          {(!filteredKnowledge || !filteredKnowledge.length) &&
            "No available knowledge"}
          {filteredKnowledge?.map((knowledge, i) => (
            <Button
              key={i}
              type="button"
              className="flex w-full items-center justify-between p-2 bg-transparent text-neutral-800 shadow-none font-semibold hover:bg-slate-200 transition-colors cursor-pointer"
              onClick={() => {
                setSelectedKnowledge(k => [...k, knowledge]);
                setOpen(false);
              }}
            >
              {knowledge.name}
            </Button>
          ))}
        </PopoverContent>
      </Popover>

      {selectedKnowledge.map((knowledge, i) => (
        <div
          key={i}
          className="flex items-center rounded-sm bg-slate-200 px-2 py-0.5 border border-slate-300 text-sm text-neutral-600"
        >
          <h3>{knowledge.name}</h3>
          <Button
            type="button"
            className="p-0 size-auto bg-transparent shadow-none text-black hover:bg-transparent cursor-pointer"
            onClick={() =>
              setSelectedKnowledge(k => k.filter(s => s.id !== knowledge.id))
            }
          >
            <X className="size-5 mt-0.5" />
          </Button>
        </div>
      ))}
    </div>
  );
};

export default DocumentSelector;
