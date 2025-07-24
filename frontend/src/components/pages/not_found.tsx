import { Button } from "@/components/ui/button";
import { useLanguage } from "@/contexts/LanguageContext";

export const NotFound: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>{t("page.not.found")}</h1>
      <p>{t("page.not.exists")}</p>

      <Button onClick={() => (window.location.href = "/")}>
        {t("page.go.home")}
      </Button>
    </div>
  );
};
