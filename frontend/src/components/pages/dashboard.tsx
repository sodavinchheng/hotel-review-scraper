import { useLanguage } from "@/contexts/LanguageContext";
import { useDashboard } from "@/hooks/useDashboard";
import { HeaderTemplate } from "../templates/HeaderTemplate";

export const Dashboard = () => {
  const { t } = useLanguage();

  const {} = useDashboard();

  return (
    <HeaderTemplate pageName="dashboard" subtitle={t("dashboard.subtitle")}>
      {t("page.loading")}
    </HeaderTemplate>
  );
};
