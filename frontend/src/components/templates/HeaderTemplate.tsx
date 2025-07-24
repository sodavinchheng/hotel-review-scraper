import { Header } from "../organisms/Header";

interface Props {
  pageName: "dashboard";
  subtitle: string;
  onBack?: () => void;
  children: React.ReactNode;
}

export const HeaderTemplate: React.FC<Props> = ({
  pageName,
  subtitle,
  onBack,
  children,
}) => {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <Header pageName={pageName} subtitle={subtitle} onBack={onBack} />

        {children}
      </div>
    </div>
  );
};
