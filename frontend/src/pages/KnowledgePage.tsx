import Spinner from "@/components/Spinner";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import useToken from "@/lib/hooks/useToken.hooks";
import {
  useCreateKnowledge,
  useDeleteKnowledge,
  useListKnowledge,
} from "@/lib/services/knowledge.service";
import { useQueryClient } from "@tanstack/react-query";
import { EllipsisVertical, Trash } from "lucide-react";
import React from "react";
import { useDropzone } from "react-dropzone";
import { toast } from "sonner";
import KnowledgeUploadHero from "./KnowledgeUploadHero";

const KnowledgeContent: React.FC = () => {
  const token = useToken();
  const queryClient = useQueryClient();

  const { data: knowledgeList } = useListKnowledge(token);

  const uploadKnowledge = useCreateKnowledge(token, queryClient);

  const deleteKnowledge = useDeleteKnowledge(token, queryClient);

  const { getRootProps, getInputProps, open, isDragActive, isDragReject } =
    useDropzone({
      noClick: true,
      maxFiles: 1,
      multiple: false,
      accept: {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
          [],
      },
      // disabled: knowledgeUpload.isPending,
      onDrop: acceptedFiles => {
        if (isDragReject) {
          toast("Unable to upload file", {
            description: "Make sure you only upload one .docx file at a time",
            duration: 5000,
          });
          return;
        }

        const data = new FormData();
        data.append("file", acceptedFiles[0]);
        toast.promise(uploadKnowledge.mutateAsync(data), {
          loading: "Loading....",
          success: resp => `${resp.name} has been added`,
          error: err => `Error: ${err.message}`,
        });
      },
    });

  if (!knowledgeList) return <h1>Loading...</h1>;

  return (
    <div
      className={`flex h-[calc(100%-40px)] w-full border-4 border-dashed transition-colors duration-300 ${knowledgeList.knowledges.length > 0 && isDragActive ? "border-foreground/50 bg-foreground/5 " : "border-transparent"}`}
      {...getRootProps()}
    >
      <input {...getInputProps()} />
      {knowledgeList.knowledges.length > 0 ? (
        <div className="px-8 pt-6 flex w-full flex-col gap-2">
          <h1 className="text-xl font-semibold">Documents</h1>
          {knowledgeList.knowledges.map((file, index) => (
            <div
              key={index}
              className="border-stronger-border-color text-foreground/80 flex w-full items-center justify-between border-b px-4 py-1 text-xs font-semibold"
            >
              <h3>{file.name}</h3>
              <div className="flex items-center">
                <h3>{Math.round(file.file_size / 1024 / 1024)} MB</h3>
                <Popover>
                  <PopoverTrigger asChild className="cursor-pointer">
                    <EllipsisVertical />
                  </PopoverTrigger>
                  <PopoverContent
                    align="end"
                    sideOffset={0}
                    className="border-stronger-border-color max-w-40 p-1"
                  >
                    <button
                      type="button"
                      onClick={() =>
                        deleteKnowledge.mutate(file.id, {
                          onSuccess: () => toast("File deleted"),
                        })
                      }
                      className="text-red-500 flex gap-2 p-2 cursor-pointer w-full"
                      disabled={deleteKnowledge.isPending}
                    >
                      {deleteKnowledge.isPending ? (
                        <Spinner className="stroke-error-red text-error-red" />
                      ) : (
                        <Trash />
                      )}{" "}
                      Delete
                    </button>
                  </PopoverContent>
                </Popover>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <KnowledgeUploadHero
          isDragActive={isDragActive}
          open={open}
          isLoading={false}
        />
      )}
    </div>
  );
};

export default KnowledgeContent;
