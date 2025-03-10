import Spinner from "@/components/Spinner";
import { Button } from "@/components/ui/button";
import { cva } from "class-variance-authority";
import { Plus, Upload } from "lucide-react";
import React from "react";

const KnowledgeUploadHero: React.FC<{
  isDragActive: boolean;
  open: () => void;
  isLoading: boolean;
}> = ({ isDragActive, open, isLoading }) => {
  const dragUploadVariant = cva(
    "transition-color m-8 flex size-full flex-col items-center justify-center rounded-xl border-4 border-dashed duration-500 ease-in-out",
    {
      variants: {
        variant: {
          default: "border-foreground/30",
          dragging: "border-foreground/80 bg-foreground/5",
        },
      },
      defaultVariants: {
        variant: "default",
      },
    },
  );

  return (
    <div
      className={dragUploadVariant({
        variant: isDragActive ? "dragging" : "default",
      })}
    >
      <button
        type="button"
        onClick={e => {
          e.stopPropagation();
          open!();
        }}
        disabled={isLoading}
        className="cursor-pointer"
      >
        {isLoading ? (
          <Spinner className="size-10 invert" />
        ) : (
          <Upload className="mx-auto size-12 text-black" />
        )}
      </button>
      <h3 className="mt-2 text-sm text-gray-600">
        {isLoading
          ? "Uploading file..."
          : "Drag and drop some files here, or click to select files"}
      </h3>
      <h3 className="mt-1 text-xs text-gray-500">
        (Only .docx files will be accepted)
      </h3>
      {!isLoading && (
        <Button
          type="button"
          onClick={e => {
            e.stopPropagation();
            open!();
          }}
          className="bg-foreground mt-4 flex justify-center gap-1 rounded-md text-xs text-white cursor-pointer"
        >
          <Plus className="size-5" /> Add File
        </Button>
      )}
    </div>
  );
};

export default KnowledgeUploadHero;
