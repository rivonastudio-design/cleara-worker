# Messages for every finding code in 4 languages. {v}=found value, {e}=expected value
M = {
"bleed_missing": {
 "en": ("Bleed is {v}, needs {e}.", "Extend background/images 3 mm beyond the trim line and re-export with bleed."),
 "hi": ("ब्लीड {v} है, {e} चाहिए।", "बैकग्राउंड/इमेज को ट्रिम लाइन से 3 मिमी बाहर तक बढ़ाएँ और ब्लीड के साथ दोबारा एक्सपोर्ट करें।"),
 "gu": ("બ્લીડ {v} છે, {e} જોઈએ.", "બેકગ્રાઉન્ડ/ઇમેજને ટ્રિમ લાઇનથી 3 મિમી બહાર સુધી વધારો અને બ્લીડ સાથે ફરી એક્સપોર્ટ કરો."),
 "hinglish": ("Bleed {v} hai, {e} chahiye.", "Background/image ko trim line se 3 mm bahar tak badhao aur bleed ke saath dobara export karo.")},
"bleed_unknown": {
 "en": ("Could not detect trim/bleed boxes in this PDF. Please confirm bleed is included.", "Export the PDF with crop marks or TrimBox/BleedBox set."),
 "hi": ("इस PDF में ट्रिम/ब्लीड बॉक्स नहीं मिला। कृपया पुष्टि करें कि ब्लीड शामिल है।", "PDF को क्रॉप मार्क्स या TrimBox/BleedBox के साथ एक्सपोर्ट करें।"),
 "gu": ("આ PDF માં ટ્રિમ/બ્લીડ બોક્સ મળ્યું નથી. કૃપા કરી ખાતરી કરો કે બ્લીડ શામેલ છે.", "PDF ને ક્રોપ માર્ક્સ અથવા TrimBox/BleedBox સાથે એક્સપોર્ટ કરો."),
 "hinglish": ("Is PDF me trim/bleed box nahi mila. Confirm karo ki bleed hai.", "PDF ko crop marks ya TrimBox/BleedBox ke saath export karo.")},
"safe_margin": {
 "en": ("Text/object is {v} from the trim edge, needs at least {e}.", "Move important text and logos inside the safe margin."),
 "hi": ("टेक्स्ट/ऑब्जेक्ट कट एज से {v} दूर है, कम से कम {e} चाहिए।", "ज़रूरी टेक्स्ट और लोगो को सेफ मार्जिन के अंदर रखें।"),
 "gu": ("ટેક્સ્ટ/ઑબ્જેક્ટ કટ એજથી {v} દૂર છે, ઓછામાં ઓછું {e} જોઈએ.", "મહત્વનું ટેક્સ્ટ અને લોગો સેફ માર્જિનની અંદર રાખો."),
 "hinglish": ("Text/object cut edge se {v} door hai, kam se kam {e} chahiye.", "Zaruri text aur logo safe margin ke andar rakho.")},
"rgb_color": {
 "en": ("RGB colour found ({v}). Print needs CMYK.", "Convert the file to CMYK before exporting."),
 "hi": ("RGB रंग मिला ({v})। प्रिंट के लिए CMYK चाहिए।", "एक्सपोर्ट से पहले फ़ाइल को CMYK में बदलें।"),
 "gu": ("RGB રંગ મળ્યો ({v}). પ્રિન્ટ માટે CMYK જોઈએ.", "એક્સપોર્ટ પહેલાં ફાઇલ CMYK માં બદલો."),
 "hinglish": ("RGB color mila ({v}). Print ke liye CMYK chahiye.", "Export se pehle file ko CMYK me convert karo.")},
"low_dpi": {
 "en": ("Image resolution is {v} (needs {e}). It will print blurry.", "Use a higher-resolution original image."),
 "hi": ("इमेज रेज़ोल्यूशन {v} है ({e} चाहिए)। प्रिंट धुंधला आएगा।", "ज़्यादा रेज़ोल्यूशन वाली ओरिजिनल इमेज इस्तेमाल करें।"),
 "gu": ("ઇમેજ રિઝોલ્યુશન {v} છે ({e} જોઈએ). પ્રિન્ટ ઝાંખું આવશે.", "વધુ રિઝોલ્યુશનવાળી મૂળ ઇમેજ વાપરો."),
 "hinglish": ("Image resolution {v} hai ({e} chahiye). Print blur aayega.", "Zyada resolution wali original image use karo.")},
"font_not_embedded": {
 "en": ("Font '{v}' is not embedded. It may change on the printer's computer.", "Embed all fonts or convert text to outlines."),
 "hi": ("फ़ॉन्ट '{v}' एम्बेड नहीं है। प्रिंटर के कंप्यूटर पर बदल सकता है।", "सभी फ़ॉन्ट एम्बेड करें या टेक्स्ट को आउटलाइन में बदलें।"),
 "gu": ("ફોન્ટ '{v}' એમ્બેડ નથી. પ્રિન્ટરના કમ્પ્યુટર પર બદલાઈ શકે છે.", "બધા ફોન્ટ એમ્બેડ કરો અથવા ટેક્સ્ટને આઉટલાઇનમાં ફેરવો."),
 "hinglish": ("Font '{v}' embed nahi hai. Printer ke computer par badal sakta hai.", "Saare fonts embed karo ya text ko outline me convert karo.")},
"small_text": {
 "en": ("Text is {v}, smaller than {e}. May be unreadable in print.", "Increase the text size."),
 "hi": ("टेक्स्ट {v} है, {e} से छोटा। प्रिंट में पढ़ना मुश्किल हो सकता है।", "टेक्स्ट का साइज़ बढ़ाएँ।"),
 "gu": ("ટેક્સ્ટ {v} છે, {e} કરતાં નાનું. પ્રિન્ટમાં વાંચવું મુશ્કેલ થઈ શકે.", "ટેક્સ્ટનું સાઇઝ વધારો."),
 "hinglish": ("Text {v} hai, {e} se chhota. Print me padhna mushkil ho sakta hai.", "Text ka size badhao.")},
"hairline": {
 "en": ("Line is {v} thick, thinner than {e}. May not print.", "Make the line at least 0.25 pt."),
 "hi": ("लाइन {v} मोटी है, {e} से पतली। प्रिंट न हो सकती है।", "लाइन कम से कम 0.25 pt रखें।"),
 "gu": ("લાઇન {v} જાડી છે, {e} કરતાં પાતળી. પ્રિન્ટ ન થઈ શકે.", "લાઇન ઓછામાં ઓછી 0.25 pt રાખો."),
 "hinglish": ("Line {v} moti hai, {e} se patli. Print na ho sakti hai.", "Line kam se kam 0.25 pt rakho.")},
"transparency": {
 "en": ("Transparency/opacity effects found.", "Flatten transparency or export as PDF/X-1a."),
 "hi": ("ट्रांसपेरेंसी/ओपेसिटी इफ़ेक्ट मिले।", "ट्रांसपेरेंसी फ्लैटन करें या PDF/X-1a में एक्सपोर्ट करें।"),
 "gu": ("ટ્રાન્સપરન્સી/ઓપેસિટી ઇફેક્ટ મળ્યા.", "ટ્રાન્સપરન્સી ફ્લેટન કરો અથવા PDF/X-1a માં એક્સપોર્ટ કરો."),
 "hinglish": ("Transparency/opacity effect mile.", "Transparency flatten karo ya PDF/X-1a me export karo.")},
"overprint": {
 "en": ("Overprint is set. Please confirm it is intended.", "Turn off overprint unless the printer asked for it."),
 "hi": ("ओवरप्रिंट सेट है। कृपया पुष्टि करें कि यह जानबूझकर है।", "प्रिंटर ने न कहा हो तो ओवरप्रिंट बंद करें।"),
 "gu": ("ઓવરપ્રિન્ટ સેટ છે. કૃપા કરી ખાતરી કરો કે તે જાણી જોઈને છે.", "પ્રિન્ટરે ન કહ્યું હોય તો ઓવરપ્રિન્ટ બંધ કરો."),
 "hinglish": ("Overprint set hai. Confirm karo ki ye jaanbujh kar hai.", "Printer ne na kaha ho to overprint band karo.")},
"spot_color": {
 "en": ("Spot colour '{v}' found. Please confirm it is meant for a special ink/finish.", "Check this layer is for Spot UV/Foil/Die-cut/Pantone as intended."),
 "hi": ("स्पॉट कलर '{v}' मिला। कृपया पुष्टि करें कि यह खास इंक/फिनिश के लिए है।", "जाँचें कि यह Spot UV/Foil/Die-cut/Pantone के लिए ही है।"),
 "gu": ("સ્પોટ કલર '{v}' મળ્યો. કૃપા કરી ખાતરી કરો કે તે ખાસ ઇંક/ફિનિશ માટે છે.", "તપાસો કે આ Spot UV/Foil/Die-cut/Pantone માટે જ છે."),
 "hinglish": ("Spot color '{v}' mila. Confirm karo ki ye special ink/finish ke liye hai.", "Check karo ye Spot UV/Foil/Die-cut/Pantone ke liye hi hai.")},
"registration_black": {
 "en": ("Registration black (100% on all inks) used.", "Use 100K black or a rich black instead."),
 "hi": ("रजिस्ट्रेशन ब्लैक (सभी इंक 100%) इस्तेमाल हुआ।", "इसकी जगह 100K ब्लैक या रिच ब्लैक इस्तेमाल करें।"),
 "gu": ("રજિસ્ટ્રેશન બ્લેક (બધી ઇંક 100%) વપરાયું.", "તેના બદલે 100K બ્લેક અથવા રિચ બ્લેક વાપરો."),
 "hinglish": ("Registration black (saari ink 100%) use hua.", "Iski jagah 100K black ya rich black use karo.")},
"tac_high": {
 "en": ("Total ink coverage is {v}, above {e}. Ink may smudge.", "Reduce ink density in dark areas."),
 "hi": ("कुल इंक कवरेज {v} है, {e} से ज़्यादा। इंक फैल सकती है।", "गहरे हिस्सों में इंक डेंसिटी कम करें।"),
 "gu": ("કુલ ઇંક કવરેજ {v} છે, {e} કરતાં વધારે. ઇંક ફેલાઈ શકે.", "ઘેરા ભાગોમાં ઇંક ડેન્સિટી ઘટાડો."),
 "hinglish": ("Total ink coverage {v} hai, {e} se zyada. Ink phail sakti hai.", "Dark areas me ink density kam karo.")},
"crop_marks": {
 "en": ("No crop marks detected. Please confirm cut lines are clear.", "Add crop marks outside the bleed area."),
 "hi": ("क्रॉप मार्क्स नहीं मिले। कृपया पुष्टि करें कि कटिंग लाइन साफ़ है।", "ब्लीड के बाहर क्रॉप मार्क्स जोड़ें।"),
 "gu": ("ક્રોપ માર્ક્સ મળ્યા નથી. કૃપા કરી ખાતરી કરો કે કટિંગ લાઇન સ્પષ્ટ છે.", "બ્લીડની બહાર ક્રોપ માર્ક્સ ઉમેરો."),
 "hinglish": ("Crop marks nahi mile. Confirm karo ki cutting line clear hai.", "Bleed ke bahar crop marks add karo.")},
"size_mismatch": {
 "en": ("Page size is {v}, expected {e}.", "Resize the artwork to the selected size."),
 "hi": ("पेज साइज़ {v} है, {e} अपेक्षित।", "आर्टवर्क को चुने हुए साइज़ में बदलें।"),
 "gu": ("પેજ સાઇઝ {v} છે, {e} અપેક્ષિત.", "આર્ટવર્કને પસંદ કરેલા સાઇઝમાં બદલો."),
 "hinglish": ("Page size {v} hai, {e} expected tha.", "Artwork ko chuni hui size me badlo.")},
"corrupt": {
 "en": ("This file could not be opened. It may be corrupt or password-protected.", "Re-export the PDF and upload again. Your credits are refunded."),
 "hi": ("यह फ़ाइल खुल नहीं सकी। यह खराब या पासवर्ड वाली हो सकती है।", "PDF दोबारा एक्सपोर्ट करके अपलोड करें। आपके क्रेडिट वापस हो गए हैं।"),
 "gu": ("આ ફાઇલ ખુલી શકી નહીં. તે બગડેલી અથવા પાસવર્ડવાળી હોઈ શકે.", "PDF ફરી એક્સપોર્ટ કરીને અપલોડ કરો. તમારા ક્રેડિટ પાછા આપ્યા છે."),
 "hinglish": ("Ye file khul nahi saki. Corrupt ya password wali ho sakti hai.", "PDF dobara export karke upload karo. Aapke credits wapas ho gaye.")},
}
LANGS = ["en", "hi", "gu", "hinglish"]

def build(code, v="", e=""):
    t = M[code]
    msg = {l: t[l][0].format(v=v, e=e) for l in LANGS}
    fix = {l: t[l][1] for l in LANGS}
    return msg, fix
