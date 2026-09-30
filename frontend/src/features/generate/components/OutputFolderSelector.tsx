import { useFormContext } from "react-hook-form";
import { GenerateFormValues } from "../validation";
import { Folder } from "lucide-react";

export function OutputFolderSelector() {
  const { register, formState: { errors } } = useFormContext<GenerateFormValues>();

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-foreground">Output Folder</label>
      <div className="flex gap-2">
        <div className="relative flex-1">
          <Folder size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input 
            type="text"
            {...register("outputFolder")}
            placeholder="/path/to/output"
            className="w-full h-10 pl-9 pr-4 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>
        <button type="button" className="px-4 h-10 bg-muted hover:bg-muted/80 text-foreground font-medium rounded-md border border-border transition-colors">
          Browse
        </button>
      </div>
      {errors.outputFolder && <p className="text-xs text-destructive">{errors.outputFolder.message}</p>}
    </div>
  );
}
