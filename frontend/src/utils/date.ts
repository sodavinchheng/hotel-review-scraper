import type { Language } from "@/contexts/LanguageContext";

export const formatDateTime = (date: Date, language: Language): string => {
  // Example: "2023年1月1日 12:00"
  if (language === "ja")
    return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${date
      .getHours()
      .toString()
      .padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;

  // Example: "Jan 01, 2023 12:00 AM"
  return new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  }).format(date);
};

export const formatDate = (date: Date, language: Language): string => {
  // Example: "2023年1月1日"
  if (language === "ja")
    return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;

  // Example: "Jan 01, 2023"
  return new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "short",
    day: "2-digit",
  }).format(date);
};

export const formatYearMonth = (
  dateString: string,
  language: Language,
): string => {
  const date = new Date(dateString);
  if (language === "ja") {
    return `${date.getFullYear()}年${date.getMonth() + 1}月`;
  }
  return new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "short",
  }).format(date);
};
