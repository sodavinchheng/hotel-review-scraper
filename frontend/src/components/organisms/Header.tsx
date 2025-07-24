import { useLanguage } from "@/contexts/LanguageContext";
import { ArrowLeft } from "lucide-react";
import LanguageSwitcher from "../atoms/LanguageSwitcher";
import { Button } from "../ui/button";

interface Props {
  pageName: "dashboard";
  subtitle: string;
  onBack?: () => void;
}

export const Header: React.FC<Props> = ({ pageName, subtitle, onBack }) => {
  const { t } = useLanguage();

  return (
    <div className="flex md:flex-row flex-col items-start md:items-center justify-between mb-8">
      <div className="flex md:flex-row flex-col items-start md:items-center gap-4">
        {onBack !== undefined && (
          <Button variant="outline" onClick={onBack} size="sm">
            <ArrowLeft className="h-4 w-4" />
            {t(`${pageName}.back`)}
          </Button>
        )}

        <div>
          <h1 className="text-3xl font-bold text-foreground">
            {t(`${pageName}.title`)}
          </h1>
          <p className="text-muted-foreground">{subtitle}</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <LanguageSwitcher />
      </div>
    </div>
  );
};
