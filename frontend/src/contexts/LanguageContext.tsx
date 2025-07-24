import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

export type Language = "en" | "ja";

interface LanguageContextType {
  language: Language | null;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(
  undefined,
);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [language, setLanguage] = useState<Language | null>(null);
  const [translations, setTranslations] = useState<Record<string, any>>({});

  useEffect(() => {
    if (!language) {
      // Check url query parameter for language
      const urlParams = new URLSearchParams(window.location.search);
      const lang = urlParams.get("lang") as Language;

      if (lang && (lang === "en" || lang === "ja")) setLanguage(lang);
      else {
        // Check local storage for language
        const storedLang = localStorage.getItem("language") as Language;
        if (storedLang && (storedLang === "en" || storedLang === "ja")) {
          setLanguage(storedLang);
        } else setLanguage("en"); // Default to English if no language is set
      }
      return;
    }

    // Save language to local storage
    if (language) localStorage.setItem("language", language);

    fetch(`/assets/lang/${language}.json`)
      .then((response) => response.json())
      .then((data) => setTranslations(data))
      .catch((error) => {
        console.error("Error loading translations:", error);
        return {};
      });
  }, [language]);

  const t = (key: string): string => {
    if (!translations) {
      console.warn(`Translation for language "${language}" not loaded.`);
      return key; // Fallback to key i  f translation is not available
    }

    return translations[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
};
