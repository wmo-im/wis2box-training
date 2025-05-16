document.addEventListener("DOMContentLoaded", function () {
  const defaultLang = "en";
  const currentLang = document.documentElement.lang || "en";

  const aiDisclaimersTtitle = {
    en: "Disclaimer: ",
    es: "Aviso: ",
    ru: "Отказ от ответственности: ",
    ar: "تنويه: ",
    fr: "Avertissement : ",
    it: "Avviso: ",
    de: "Haftungsausschluss: ",
    zh: "免责声明：",
    pt: "Aviso: ",
  };

  const aiDisclaimers = {
    en: "This translation was generated using an AI model (OpenAI GPT-4). While we strive for accuracy, there may be errors or inconsistencies. For authoritative information, please refer to the original English version.",
    es: "Esta traducción fue generada utilizando un modelo de inteligencia artificial (OpenAI GPT-4). Aunque nos esforzamos por la precisión, pueden existir errores o inconsistencias. Para información oficial, consulte la versión original en inglés.",
    pt: "Esta tradução foi gerada usando um modelo de IA (OpenAI GPT-4). Embora nos esforcemos para garantir a precisão, podem ocorrer erros ou inconsistências. Para informações oficiais, consulte a versão original em inglês.",
    ru: "Этот перевод был сгенерирован с помощью модели искусственного интеллекта (OpenAI GPT-4). Хотя мы стремимся к точности, возможны ошибки или несоответствия. Для получения достоверной информации обратитесь к оригинальной версии на английском языке.",
    ar: "تم إنشاء هذا الترجمة باستخدام نموذج ذكاء اصطناعي (OpenAI GPT-4). على الرغم من حرصنا على الدقة، قد توجد أخطاء أو تناقضات. للحصول على المعلومات الموثوقة، يُرجى الرجوع إلى النسخة الأصلية باللغة الإنجليزية.",
    fr: "Cette traduction a été générée à l'aide d'un modèle d'IA (OpenAI GPT-4). Bien que nous nous efforcions d'assurer l'exactitude, des erreurs ou des incohérences peuvent subsister. Pour des informations officielles, veuillez consulter la version originale en anglais.",
    it: "Questa traduzione è stata generata utilizzando un modello di intelligenza artificiale (OpenAI GPT-4). Sebbene ci impegniamo per l'accuratezza, potrebbero esserci errori o incoerenze. Per informazioni ufficiali, fare riferimento alla versione originale in inglese.",
    de: "Diese Übersetzung wurde mit einem KI-Modell (OpenAI GPT-4) erstellt. Obwohl wir um Genauigkeit bemüht sind, können Fehler oder Unstimmigkeiten auftreten. Für verbindliche Informationen beachten Sie bitte die englische Originalversion.",
    zh: "本翻译由人工智能模型（OpenAI GPT-4）生成。尽管我们力求准确，但可能仍存在错误或不一致。如需权威信息，请参阅英文原始版本。",
  };

  const disclaimerKey = `ai_disclaimer_dismissed_${currentLang}`;

  if (currentLang !== defaultLang && !sessionStorage.getItem(disclaimerKey)) {
    sessionStorage.setItem(disclaimerKey, "true");
    const banner = document.createElement("div");
    banner.id = "ai-disclaimer-banner";
    banner.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 20px;
      right: 20px;
      background-color: #f9edbe;
      color: black;
      padding: 1em;
      border: 1px solid #f0c36d;
      box-shadow : 0 2px 5px rgba(0,0,0,0.2)
      z-index: 1000;
      font-size: 1.4em;
      border-radius : 8px;
    `;
    banner.innerHTML = `<span style="color: black;font-weight: bold;">${
      aiDisclaimersTtitle[currentLang]
    }</span>
      ${aiDisclaimers[currentLang] || aiDisclaimers["en"]}
      <button style="margin-left: 1em;" onclick="
        localStorage.setItem('${disclaimerKey}', 'true');
        document.getElementById('ai-disclaimer-banner').remove();
      ">Dismiss</button>
    `;
    document.body.appendChild(banner);
  }
});
