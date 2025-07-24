import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useLanguage } from "@/contexts/LanguageContext";
import { Globe } from "lucide-react";

const LanguageSwitcher = () => {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="flex items-center gap-2">
      <Globe className="h-4 w-4 text-muted-foreground" />
      <Select
        value={language ?? "en"}
        onValueChange={(value) => setLanguage(value as "en" | "ja")}
      >
        <SelectTrigger className="w-30 h-8">
          <SelectValue />
        </SelectTrigger>

        <SelectContent>
          <SelectItem value="en">🇬🇧 English</SelectItem>
          <SelectItem value="ja">🇯🇵 日本語</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};

export default LanguageSwitcher;
