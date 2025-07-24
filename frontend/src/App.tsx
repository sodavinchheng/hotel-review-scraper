import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Dashboard } from "./components/pages/dashboard";
import { NotFound } from "./components/pages/not_found";
import { LanguageProvider } from "./contexts/LanguageContext";

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
