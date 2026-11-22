# Messages for every finding code in 4 languages. {v}=found value, {e}=expected value
M = {
"bleed_missing": {
 "en": ("Bleed is {v}, needs {e}. Bleed is the extra design that goes past the cutting line. Without it a white strip can show on the edge after cutting.", "Extend the background/photo {e} beyond the cutting line on every side and export again."),
 "hi": ("ब्लीड {v} है, {e} चाहिए। ब्लीड यानी कटिंग लाइन के बाहर तक जाने वाला एक्स्ट्रा डिज़ाइन। इसके बिना कटिंग के बाद किनारे पर सफ़ेद पट्टी दिख सकती है।", "बैकग्राउंड/फ़ोटो को हर तरफ़ कटिंग लाइन से {e} बाहर तक बढ़ाएँ और दोबारा एक्सपोर्ट करें।"),
 "gu": ("બ્લીડ {v} છે, {e} જોઈએ. બ્લીડ એટલે કટિંગ લાઇનની બહાર સુધી જતી વધારાની ડિઝાઇન. તેના વગર કટિંગ પછી કિનારે સફેદ પટ્ટી દેખાઈ શકે.", "બેકગ્રાઉન્ડ/ફોટોને દરેક બાજુ કટિંગ લાઇનથી {e} બહાર સુધી વધારો અને ફરી એક્સપોર્ટ કરો."),
 "hinglish": ("Bleed {v} hai, {e} chahiye. Bleed matlab cutting line ke bahar tak jaane wala extra design. Iske bina cutting ke baad kinare pe safed patti dikh sakti hai.", "Background/photo ko har taraf cutting line se {e} bahar tak badhao aur dobara export karo.")},
"bleed_unknown": {
 "en": ("The design touches the edge, but the file does not say where the cutting line is. Please confirm bleed (extra design past the cutting line) is included.", "Check that the background goes {e} past the cutting line on every side."),
 "hi": ("डिज़ाइन किनारे तक है, पर फ़ाइल में कटिंग लाइन की जानकारी नहीं है। कृपया पुष्टि करें कि ब्लीड (कटिंग लाइन के बाहर का एक्स्ट्रा डिज़ाइन) शामिल है।", "जाँचें कि बैकग्राउंड हर तरफ़ कटिंग लाइन से {e} बाहर तक है।"),
 "gu": ("ડિઝાઇન કિનારા સુધી છે, પણ ફાઇલમાં કટિંગ લાઇનની માહિતી નથી. કૃપા કરી ખાતરી કરો કે બ્લીડ (કટિંગ લાઇનની બહારની વધારાની ડિઝાઇન) શામેલ છે.", "તપાસો કે બેકગ્રાઉન્ડ દરેક બાજુ કટિંગ લાઇનથી {e} બહાર સુધી છે."),
 "hinglish": ("Design kinare tak hai, par file me cutting line ki jaankari nahi hai. Confirm karo ki bleed (cutting line ke bahar ka extra design) rakha hai.", "Check karo ki background har taraf cutting line se {e} bahar tak hai.")},
"cut_overlap": {
 "en": ("Shape-cutting job: design goes only {v} past the cutting line, needs at least {e}. If the cut shifts even a little, the print will look bad.", "Extend the design at least {e} beyond the cutting line."),
 "hi": ("शेप कटिंग जॉब: डिज़ाइन कटिंग लाइन से सिर्फ़ {v} बाहर है, कम से कम {e} चाहिए। कटिंग थोड़ी भी हिली तो प्रिंट ख़राब दिखेगा।", "डिज़ाइन को कटिंग लाइन से कम से कम {e} बाहर तक बढ़ाएँ।"),
 "gu": ("શેપ કટિંગ જોબ: ડિઝાઇન કટિંગ લાઇનથી ફક્ત {v} બહાર છે, ઓછામાં ઓછું {e} જોઈએ. કટિંગ થોડું પણ ખસે તો પ્રિન્ટ ખરાબ દેખાશે.", "ડિઝાઇનને કટિંગ લાઇનથી ઓછામાં ઓછું {e} બહાર સુધી વધારો."),
 "hinglish": ("Shape cutting job: design cutting line se sirf {v} bahar hai, kam se kam {e} chahiye. Cutting thodi bhi hili to print kharab dikhega.", "Design ko cutting line se kam se kam {e} bahar tak badhao.")},
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
 "en": ("Image resolution is {v} (needs {e}). It will print blurry.", "Use a higher-resolution original image. If several images have this issue, select them all together and convert/bitmap them to 300+ dpi in one go instead of doing each one separately."),
 "hi": ("इमेज रेज़ोल्यूशन {v} है ({e} चाहिए)। प्रिंट धुंधला आएगा।", "ज़्यादा रेज़ोल्यूशन वाली ओरिजिनल इमेज इस्तेमाल करें। अगर कई इमेज में यह समस्या है, तो सभी को एक साथ सेलेक्ट करके एक बार में 300+ dpi पर बिटमैप/कन्वर्ट करें, एक-एक अलग करने की ज़रूरत नहीं।"),
 "gu": ("ઇમેજ રિઝોલ્યુશન {v} છે ({e} જોઈએ). પ્રિન્ટ ઝાંખું આવશે.", "વધુ રિઝોલ્યુશનવાળી મૂળ ઇમેજ વાપરો. જો અનેક ઇમેજમાં આ સમસ્યા હોય, તો બધાને સાથે સિલેક્ટ કરીને એક જ વારમાં 300+ dpi પર બિટમેપ/કન્વર્ટ કરો, એક-એક અલગ કરવાની જરૂર નથી."),
 "hinglish": ("Image resolution {v} hai ({e} chahiye). Print blur aayega.", "Zyada resolution wali original image use karo. Agar multiple images mein ye problem hai, to sabko ek saath select karke 300+ dpi pe ek baar mein bitmap/convert karo — ek-ek alag karne ki zaroorat nahi.")},
"font_not_embedded": {
 "en": ("Font '{v}' is not embedded or converted. It may change on the printer's computer.", "Convert text to curves/outlines or embed all fonts."),
 "hi": ("फ़ॉन्ट '{v}' एम्बेड या कन्वर्ट नहीं है। प्रिंटर के कंप्यूटर पर बदल सकता है।", "टेक्स्ट को कर्व/आउटलाइन में बदलें या सभी फ़ॉन्ट एम्बेड करें।"),
 "gu": ("ફોન્ટ '{v}' એમ્બેડ કે કન્વર્ટ નથી. પ્રિન્ટરના કમ્પ્યુટર પર બદલાઈ શકે છે.", "ટેક્સ્ટને કર્વ/આઉટલાઇનમાં ફેરવો અથવા બધા ફોન્ટ એમ્બેડ કરો."),
 "hinglish": ("Font '{v}' embed ya convert nahi hai. Printer ke computer par badal sakta hai.", "Text ko curve/outline me convert karo ya saare fonts embed karo.")},
"small_text": {
 "en": ("Text is {v}, smaller than {e}. May be unreadable in print.", "Increase the text size."),
 "hi": ("टेक्स्ट {v} है, {e} से छोटा। प्रिंट में पढ़ना मुश्किल हो सकता है।", "टेक्स्ट का साइज़ बढ़ाएँ।"),
 "gu": ("ટેક્સ્ટ {v} છે, {e} કરતાં નાનું. પ્રિન્ટમાં વાંચવું મુશ્કેલ થઈ શકે.", "ટેક્સ્ટનું સાઇઝ વધારો."),
 "hinglish": ("Text {v} hai, {e} se chhota. Print me padhna mushkil ho sakta hai.", "Text ka size badhao.")},
"scanned_maybe_blurry": {
 "en": ("This page looks like a scanned/flattened picture, not real text. We can't check if any text inside it is too small or blurry.", "Open the picture and zoom in — if text looks blurry or too small, rescan at a higher resolution or recreate it with real text."),
 "hi": ("ये पेज स्कैन/फ्लैट की गई तस्वीर जैसा लग रहा है, असली टेक्स्ट नहीं। इसके अंदर का टेक्स्ट छोटा या ब्लर है या नहीं, ये हम चेक नहीं कर सकते।", "तस्वीर खोलकर ज़ूम करके देखें — अगर टेक्स्ट ब्लर या बहुत छोटा लगे, तो ज़्यादा resolution में फिर से स्कैन करें या असली टेक्स्ट से बनाएँ।"),
 "gu": ("આ પેજ સ્કેન/ફ્લેટ કરેલી તસવીર જેવું લાગે છે, સાચું ટેક્સ્ટ નથી. તેની અંદરનું ટેક્સ્ટ નાનું કે બ્લર છે કે નહીં, તે અમે ચેક કરી શકતા નથી.", "તસવીર ખોલીને ઝૂમ કરીને જુઓ — ટેક્સ્ટ બ્લર કે બહુ નાનું લાગે તો વધુ resolution માં ફરી સ્કેન કરો અથવા સાચા ટેક્સ્ટથી બનાવો."),
 "hinglish": ("Ye page scan/flatten ki hui picture jaisa lag raha hai, real text nahi. Iske andar ka text chhota ya blur hai ya nahi, ye hum check nahi kar sakte.", "Picture khol ke zoom karo — agar text blur ya bahut chhota lage, to zyada resolution me firse scan karo ya real text se banao.")},
"thin_font_small": {
 "en": ("Text is {v}, a thin/light font close to the {e} limit. Thin strokes at this size may look broken or go missing in print.", "Use a regular/bold weight instead of a thin/light font, or increase the text size."),
 "hi": ("टेक्स्ट {v} है, एक पतला/लाइट फ़ॉन्ट {e} लिमिट के पास। इस साइज़ में पतली लाइनें प्रिंट में टूटी या गायब दिख सकती हैं।", "पतले/लाइट फ़ॉन्ट की जगह रेगुलर/बोल्ड इस्तेमाल करें, या टेक्स्ट साइज़ बढ़ाएँ।"),
 "gu": ("ટેક્સ્ટ {v} છે, પાતળો/લાઇટ ફોન્ટ {e} લિમિટની નજીક. આ સાઇઝમાં પાતળી લાઇનો પ્રિન્ટમાં તૂટેલી અથવા ગાયબ દેખાઈ શકે.", "પાતળા/લાઇટ ફોન્ટને બદલે રેગ્યુલર/બોલ્ડ વાપરો, અથવા ટેક્સ્ટ સાઇઝ વધારો."),
 "hinglish": ("Text {v} hai, ek thin/light font {e} limit ke paas. Is size me patli lines print me tooti ya gayab dikh sakti hain.", "Thin/light font ki jagah regular/bold use karo, ya text size badhao.")},
"hairline": {
 "en": ("Line is {v} thick, thinner than {e}. May not print.", "Make the line at least {e}."),
 "hi": ("लाइन {v} मोटी है, {e} से पतली। प्रिंट न हो सकती है।", "लाइन कम से कम {e} रखें।"),
 "gu": ("લાઇન {v} જાડી છે, {e} કરતાં પાતળી. પ્રિન્ટ ન થઈ શકે.", "લાઇન ઓછામાં ઓછી {e} રાખો."),
 "hinglish": ("Line {v} moti hai, {e} se patli. Print na ho sakti hai.", "Line kam se kam {e} rakho.")},
"transparency": {
 "en": ("Transparency/opacity effects found.", "Flatten transparency (convert to bitmap) or export as PDF/X-1a."),
 "hi": ("ट्रांसपेरेंसी/ओपेसिटी इफ़ेक्ट मिले।", "ट्रांसपेरेंसी फ्लैटन करें (बिटमैप में बदलें) या PDF/X-1a में एक्सपोर्ट करें।"),
 "gu": ("ટ્રાન્સપરન્સી/ઓપેસિટી ઇફેક્ટ મળ્યા.", "ટ્રાન્સપરન્સી ફ્લેટન કરો (બિટમેપમાં ફેરવો) અથવા PDF/X-1a માં એક્સપોર્ટ કરો."),
 "hinglish": ("Transparency/opacity effect mile.", "Transparency flatten karo (bitmap me convert karo) ya PDF/X-1a me export karo.")},
"overprint": {
 "en": ("Overprint is set. Please confirm it is intended.", "Turn off overprint unless the printer asked for it."),
 "hi": ("ओवरप्रिंट सेट है। कृपया पुष्टि करें कि यह जानबूझकर है।", "प्रिंटर ने न कहा हो तो ओवरप्रिंट बंद करें।"),
 "gu": ("ઓવરપ્રિન્ટ સેટ છે. કૃપા કરી ખાતરી કરો કે તે જાણી જોઈને છે.", "પ્રિન્ટરે ન કહ્યું હોય તો ઓવરપ્રિન્ટ બંધ કરો."),
 "hinglish": ("Overprint set hai. Confirm karo ki ye jaanbujh kar hai.", "Printer ne na kaha ho to overprint band karo.")},
"white_overprint": {
 "en": ("White colour is set to overprint. It will disappear in print.", "Turn off overprint on white text/objects."),
 "hi": ("सफ़ेद रंग पर ओवरप्रिंट सेट है। प्रिंट में यह ग़ायब हो जाएगा।", "सफ़ेद टेक्स्ट/ऑब्जेक्ट पर ओवरप्रिंट बंद करें।"),
 "gu": ("સફેદ રંગ પર ઓવરપ્રિન્ટ સેટ છે. પ્રિન્ટમાં તે ગાયબ થઈ જશે.", "સફેદ ટેક્સ્ટ/ઑબ્જેક્ટ પર ઓવરપ્રિન્ટ બંધ કરો."),
 "hinglish": ("Safed color pe overprint set hai. Print me ye gayab ho jayega.", "Safed text/object pe overprint band karo.")},
"spot_color": {
 "en": ("Special colour '{v}' found (gold, silver, Pantone or other 5th colour). A normal CMYK job cannot print it.", "Convert it to CMYK, or tell the printer this job needs a special ink."),
 "hi": ("स्पेशल कलर '{v}' मिला (गोल्ड, सिल्वर, पैनटोन या कोई 5वाँ कलर)। सामान्य CMYK जॉब में यह प्रिंट नहीं होगा।", "इसे CMYK में बदलें, या प्रिंटर को बताएँ कि इस जॉब में स्पेशल इंक चाहिए।"),
 "gu": ("સ્પેશિયલ કલર '{v}' મળ્યો (ગોલ્ડ, સિલ્વર, પેન્ટોન કે અન્ય 5મો કલર). સામાન્ય CMYK જોબમાં તે પ્રિન્ટ નહીં થાય.", "તેને CMYK માં બદલો, અથવા પ્રિન્ટરને જણાવો કે આ જોબમાં સ્પેશિયલ ઇંક જોઈએ."),
 "hinglish": ("Special color '{v}' mila (gold, silver, pantone ya koi 5th color). Normal CMYK job me ye print nahi hoga.", "Ise CMYK me convert karo, ya printer ko batao ki is job me special ink chahiye.")},
"registration_black": {
 "en": ("Registration colour (100% on all 4 inks) used in the design.", "Use 100K black instead."),
 "hi": ("डिज़ाइन में रजिस्ट्रेशन कलर (चारों इंक 100%) इस्तेमाल हुआ।", "इसकी जगह 100K ब्लैक इस्तेमाल करें।"),
 "gu": ("ડિઝાઇનમાં રજિસ્ટ્રેશન કલર (ચારેય ઇંક 100%) વપરાયો.", "તેના બદલે 100K બ્લેક વાપરો."),
 "hinglish": ("Design me registration color (charon ink 100%) use hua.", "Iski jagah 100K black use karo.")},
"tac_high": {
 "en": ("Total ink is {v}, above {e}. Ink may smudge or not dry.", "Reduce ink in the dark areas."),
 "hi": ("कुल इंक {v} है, {e} से ज़्यादा। इंक फैल सकती है या सूखेगी नहीं।", "गहरे हिस्सों में इंक कम करें।"),
 "gu": ("કુલ ઇંક {v} છે, {e} કરતાં વધારે. ઇંક ફેલાઈ શકે અથવા સુકાશે નહીં.", "ઘેરા ભાગોમાં ઇંક ઘટાડો."),
 "hinglish": ("Total ink {v} hai, {e} se zyada. Ink phail sakti hai ya sookhegi nahi.", "Dark areas me ink kam karo.")},
"k_heavy": {
 "en": ("In about {v} of the design, black (K) is above {e} inside mixed colours. Colours/design may print darker than on screen.", "Check once. Reduce K in photos/colours if it should not look dark."),
 "hi": ("डिज़ाइन के लगभग {v} हिस्से में मिक्स कलर के अंदर ब्लैक (K) {e} से ज़्यादा है। रंग/डिज़ाइन स्क्रीन से ज़्यादा गहरा छप सकता है।", "एक बार देख लें। गहरा नहीं चाहिए तो फ़ोटो/रंगों में K कम करें।"),
 "gu": ("ડિઝાઇનના લગભગ {v} ભાગમાં મિક્સ કલરની અંદર બ્લેક (K) {e} કરતાં વધારે છે. રંગ/ડિઝાઇન સ્ક્રીન કરતાં વધુ ઘેરી છપાઈ શકે.", "એક વાર જોઈ લો. ઘેરું ન જોઈએ તો ફોટો/રંગોમાં K ઘટાડો."),
 "hinglish": ("Design ke lagbhag {v} hisse me mix color ke andar black (K) {e} se zyada hai. Color/design screen se zyada dark chhap sakta hai.", "Ek baar dekh lo. Dark nahi chahiye to photo/colors me K kam karo.")},
"crop_marks": {
 "en": ("The page is bigger than the job size and has no cutting marks. Please confirm the cutting position is clear.", "Add crop marks, or export at the exact size with bleed."),
 "hi": ("पेज जॉब साइज़ से बड़ा है और कटिंग मार्क्स नहीं हैं। कृपया पुष्टि करें कि कटिंग की जगह साफ़ है।", "क्रॉप मार्क्स जोड़ें, या ब्लीड के साथ सही साइज़ में एक्सपोर्ट करें।"),
 "gu": ("પેજ જોબ સાઇઝ કરતાં મોટું છે અને કટિંગ માર્ક્સ નથી. કૃપા કરી ખાતરી કરો કે કટિંગની જગ્યા સ્પષ્ટ છે.", "ક્રોપ માર્ક્સ ઉમેરો, અથવા બ્લીડ સાથે સાચા સાઇઝમાં એક્સપોર્ટ કરો."),
 "hinglish": ("Page job size se bada hai aur cutting marks nahi hain. Confirm karo ki cutting ki jagah clear hai.", "Crop marks add karo, ya bleed ke saath sahi size me export karo.")},
"sheet_marks_missing": {
 "en": ("Mixed-job sheet has no cutting marks/details. The cutter will not know where to cut.", "Add cutting marks for every job on the sheet."),
 "hi": ("मिक्स जॉब शीट में कटिंग मार्क्स/डिटेल नहीं हैं। कटिंग वाले को पता नहीं चलेगा कहाँ काटना है।", "शीट के हर जॉब के लिए कटिंग मार्क्स लगाएँ।"),
 "gu": ("મિક્સ જોબ શીટમાં કટિંગ માર્ક્સ/ડિટેલ નથી. કટિંગ કરનારને ખબર નહીં પડે ક્યાં કાપવું.", "શીટના દરેક જોબ માટે કટિંગ માર્ક્સ મૂકો."),
 "hinglish": ("Mix job sheet me cutting marks/details nahi hain. Cutting wale ko pata nahi chalega kahan kaatna hai.", "Sheet ke har job ke liye cutting marks lagao.")},
"sheet_not_grid": {
 "en": ("{v} items on this sheet are not lined up in a straight row/column grid. A straight-knife cutter can only make full straight cuts, so staggered items will not cut cleanly.", "Arrange every item on a straight row/column grid so each row and column lines up all the way across the sheet."),
 "hi": ("इस शीट पर {v} आइटम सीधी row/column grid में नहीं हैं। सीधी चाकू (straight-knife) से सिर्फ़ पूरी सीधी कट लग सकती है, इसलिए टेढ़े-मेढ़े रखे आइटम सही नहीं कटेंगे।", "हर आइटम को सीधी row/column grid में रखें ताकि हर row और column पूरी शीट में सीधी लाइन में मिले।"),
 "gu": ("આ શીટ પર {v} આઇટમ સીધી row/column ગ્રિડમાં નથી. સીધી ચપ્પુ (straight-knife) થી માત્ર પૂરો સીધો કટ થઈ શકે છે, એટલે ટેઢા-મેઢા રાખેલા આઇટમ બરાબર નહીં કપાય.", "દરેક આઇટમને સીધી row/column ગ્રિડમાં ગોઠવો જેથી દરેક row અને column પૂરી શીટમાં સીધી લાઇનમાં મળે."),
 "hinglish": ("Is sheet pe {v} items seedhi row/column grid mein nahi hain. Seedhi chhuri (straight-knife) se sirf poori seedhi cut lag sakti hai, isliye tedhe-medhe rakhe items sahi nahi katenge.", "Har item ko seedhi row/column grid mein rakho taaki har row aur column poori sheet mein seedhi line mein mile.")},
"sheet_mixed_sizes": {
 "en": ("{v} items on this sheet are different sizes. Mixing sizes makes straight-knife cutting harder and more wasteful.", "Keep all items on this sheet the same size, or cut this batch separately."),
 "hi": ("इस शीट पर {v} आइटम अलग-अलग साइज़ के हैं। साइज़ मिक्स होने से सीधी चाकू (straight-knife) से काटना मुश्किल और ज़्यादा बर्बादी वाला हो जाता है।", "शीट के सारे आइटम एक ही साइज़ के रखें, या इसे अलग से काटें।"),
 "gu": ("આ શીટ પર {v} આઇટમ અલગ-અલગ સાઇઝના છે. સાઇઝ મિક્સ થવાથી સીધી ચપ્પુ (straight-knife) થી કાપવું મુશ્કેલ અને વધુ બગાડવાળું બને છે.", "શીટના બધા આઇટમ એક જ સાઇઝના રાખો, અથવા આને અલગથી કાપો."),
 "hinglish": ("Is sheet pe {v} items alag-alag size ke hain. Size mix hone se seedhi chhuri (straight-knife) se kaatna mushkil aur zyada barbadi wala ho jata hai.", "Sheet ke saare items ek hi size ke rakho, ya ise alag se kaato.")},
"size_mismatch": {
 "en": ("File size is {v}, but the selected size is {e}.", "Resize the artwork to the selected size."),
 "hi": ("फ़ाइल साइज़ {v} है, पर चुना हुआ साइज़ {e} है।", "आर्टवर्क को चुने हुए साइज़ में बदलें।"),
 "gu": ("ફાઇલ સાઇઝ {v} છે, પણ પસંદ કરેલું સાઇઝ {e} છે.", "આર્ટવર્કને પસંદ કરેલા સાઇઝમાં બદલો."),
 "hinglish": ("File size {v} hai, par chuna hua size {e} hai.", "Artwork ko chuni hui size me badlo.")},
"qr_barcode_found": {
 "en": ("A {v} was found in this design. Print quality, size and contrast affect whether it will scan correctly -- this cannot be guaranteed from the file alone (recommended size: at least {e}).", "Print a sample copy and scan this code with a phone before printing the full batch."),
 "hi": ("इस डिज़ाइन में {v} मिला। प्रिंट क्वालिटी, साइज़ और कंट्रास्ट पर निर्भर करता है कि यह स्कैन होगा या नहीं -- सिर्फ़ फ़ाइल देखकर यह पक्का नहीं कहा जा सकता (सुझाया गया साइज़: कम से कम {e})।", "पूरी प्रिंटिंग से पहले एक सैंपल कॉपी प्रिंट करके फ़ोन से इस कोड को स्कैन करके जाँच लें।"),
 "gu": ("આ ડિઝાઇનમાં {v} મળ્યો. પ્રિન્ટ ક્વોલિટી, સાઇઝ અને કોન્ટ્રાસ્ટ પર આધાર રાખે છે કે તે સ્કેન થશે કે નહીં -- ફક્ત ફાઇલ જોઈને આ પાક્કું કહી શકાતું નથી (સૂચવેલ સાઇઝ: ઓછામાં ઓછું {e}).", "પૂરી પ્રિન્ટિંગ પહેલાં એક સેમ્પલ કોપી પ્રિન્ટ કરીને ફોનથી આ કોડને સ્કેન કરીને ચકાસો."),
 "hinglish": ("Is design mein {v} mila. Print quality, size aur contrast pe depend karta hai ki ye scan hoga ya nahi -- sirf file dekhkar ye pakka nahi kaha ja sakta (recommended size: kam se kam {e}).", "Poori printing se pehle ek sample copy print karke phone se is code ko scan karke test kar lo.")},
"row_misaligned": {
 "en": ("Content on both sides of this row (e.g. a name on one side, a phone number on the other) is not level -- one side sits slightly higher or lower than the other.", "Select both sides and use your design software's \"Align\" tool (align middle / vertical center) to bring them onto the same line."),
 "hi": ("इस row के दोनों तरफ़ की चीज़ें (जैसे एक तरफ़ नाम, दूसरी तरफ़ फ़ोन नंबर) एक लाइन में नहीं हैं -- एक तरफ़ थोड़ा ऊपर या नीचे है।", "दोनों तरफ़ को सेलेक्ट करके डिज़ाइन सॉफ़्टवेयर के \"Align\" टूल (align middle / vertical center) से एक लाइन में लाएँ।"),
 "gu": ("આ રો ની બંને બાજુની વસ્તુઓ (જેમ કે એક બાજુ નામ, બીજી બાજુ ફોન નંબર) એક લાઇનમાં નથી -- એક બાજુ થોડું ઉપર અથવા નીચે છે.", "બંને બાજુને સિલેક્ટ કરીને ડિઝાઇન સોફ્ટવેરના \"Align\" ટૂલ (align middle / vertical center) થી એક લાઇનમાં લાવો."),
 "hinglish": ("Is row ke dono taraf ki cheezein (jaise ek taraf naam, doosri taraf phone number) ek line mein nahi hain -- ek taraf thoda upar ya neeche hai.", "Dono taraf ko select karke design software ke \"Align\" tool (align middle / vertical center) se ek line mein lao.")},
"column_misaligned": {
 "en": ("These stacked lines don't all start from the same point on the left -- each one begins a little further in or out than the others.", "Select all these lines together and use \"Align Left\" so they all start from the same point."),
 "hi": ("ये एक के नीचे एक लिखी गई लाइनें सब एक ही जगह से शुरू नहीं होती -- हर एक थोड़ा आगे या पीछे से शुरू होती है।", "इन सभी लाइनों को साथ सेलेक्ट करके \"Align Left\" करें, ताकि सब एक ही जगह से शुरू हों।"),
 "gu": ("આ એક નીચે એક લખાયેલી લાઇનો બધી એક જ જગ્યાએથી શરૂ થતી નથી -- દરેક થોડું આગળ અથવા પાછળથી શરૂ થાય છે.", "આ બધી લાઇનોને સાથે સિલેક્ટ કરીને \"Align Left\" કરો, જેથી બધી એક જ જગ્યાએથી શરૂ થાય."),
 "hinglish": ("Ye ek ke neeche ek likhi gayi lines sab ek hi jagah se start nahi hoti -- har ek thoda aage ya peeche se start hoti hai.", "Ye sabhi lines ko sath select karke \"Align Left\" karo, taaki sab ek hi jagah se start ho.")},
"icon_text_misaligned": {
 "en": ("An icon and the text next to it (e.g. a phone, email or location icon with its label) are not lined up with each other vertically.", "Select the icon and its text together and use \"Align Middle\" (vertical center) so they line up."),
 "hi": ("एक icon और उसके साथ का text (जैसे phone, email या location icon और उसका लेबल) एक-दूसरे के साथ vertically लाइन में नहीं हैं।", "icon और उसके text को साथ सेलेक्ट करके \"Align Middle\" (vertical center) करें ताकि वे लाइन में आ जाएँ।"),
 "gu": ("એક icon અને તેની સાથેનો text (જેમ કે phone, email અથવા location icon અને તેનું label) એકબીજા સાથે vertically લાઇનમાં નથી.", "icon અને તેના textને સાથે સિલેક્ટ કરીને \"Align Middle\" (vertical center) કરો જેથી તે લાઇનમાં આવે."),
 "hinglish": ("Ek icon aur uske saath ka text (jaise phone, email ya location icon aur uska label) ek-doosre ke saath vertically line mein nahi hai.", "Icon aur uske text ko sath select karke \"Align Middle\" (vertical center) karo taaki wo line mein aa jaye.")},
"uneven_spacing": {
 "en": ("The gaps between these stacked lines/rows are not equal -- some gaps are bigger than others, which makes the layout look uneven.", "Select these lines together and use \"Distribute Vertically\" (or set equal line spacing) so the gaps match."),
 "hi": ("इन एक के नीचे एक lines/rows के बीच का gap बराबर नहीं है -- कोई gap बड़ा है, कोई छोटा, जिससे layout असमान दिखता है।", "इन लाइनों को साथ सेलेक्ट करके \"Distribute Vertically\" (या बराबर line spacing सेट) करें ताकि gaps बराबर हो जाएँ।"),
 "gu": ("આ એક નીચે એક lines/rows વચ્ચેનો ગેપ સરખો નથી -- કોઈ ગેપ મોટો છે, કોઈ નાનો, જેથી layout અસમાન દેખાય છે.", "આ લાઇનોને સાથે સિલેક્ટ કરીને \"Distribute Vertically\" (અથવા સરખું line spacing સેટ) કરો જેથી ગેપ સરખા થાય."),
 "hinglish": ("In ek ke neeche ek lines/rows ke beech ka gap barabar nahi hai -- koi gap bada hai, koi chhota, jisse layout asman dikhta hai.", "In lines ko sath select karke \"Distribute Vertically\" (ya barabar line spacing set) karo taaki gaps barabar ho jaye.")},
"off_center": {
 "en": ("This part of the design looks like it was meant to sit in the center, but it's shifted slightly to one side.", "Select this part and use your design software's \"Align Center\" (horizontal center) to position it exactly in the middle."),
 "hi": ("डिज़ाइन का यह हिस्सा center में होना चाहिए था, लेकिन यह थोड़ा एक तरफ़ खिसक गया है।", "इस हिस्से को सेलेक्ट करके डिज़ाइन सॉफ़्टवेयर के \"Align Center\" (horizontal center) से बीच में सही जगह पर रखें।"),
 "gu": ("ડિઝાઇનનો આ ભાગ સેન્ટરમાં હોવો જોઈતો હતો, પરંતુ તે થોડો એક બાજુ ખસી ગયો છે.", "આ ભાગને સિલેક્ટ કરીને ડિઝાઇન સોફ્ટવેરના \"Align Center\" (horizontal center) થી વચ્ચે બરાબર જગ્યાએ મૂકો."),
 "hinglish": ("Design ka ye hissa center mein hona chahiye tha, lekin ye thoda ek taraf khisak gaya hai.", "Is hisse ko select karke design software ke \"Align Center\" (horizontal center) se beech mein sahi jagah pe rakho.")},
"page_size_mixed": {
 "en": ("Page {v} is a different size from page 1 ({e}).", "Make all pages the same size."),
 "hi": ("पेज {v} का साइज़ पेज 1 ({e}) से अलग है।", "सभी पेज एक ही साइज़ के रखें।"),
 "gu": ("પેજ {v} નું સાઇઝ પેજ 1 ({e}) કરતાં અલગ છે.", "બધા પેજ એક જ સાઇઝના રાખો."),
 "hinglish": ("Page {v} ka size page 1 ({e}) se alag hai.", "Saare page ek hi size ke rakho.")},
"dark_image": {
 "en": ("Photo is very dark ({v} of it is near-black). Dark photos print even darker and shadow detail is lost.", "Brighten the photo a little (lift the shadows 10-20%) and ask for a proof before the full run."),
 "hi": ("फ़ोटो बहुत गहरी है ({v} हिस्सा लगभग काला है)। गहरी फ़ोटो प्रिंट में और ज़्यादा गहरी आती है और शैडो की डिटेल खो जाती है।", "फ़ोटो को थोड़ा हल्का करें (शैडो 10-20% उठाएँ) और पूरा प्रिंट करने से पहले प्रूफ़ मँगवाएँ।"),
 "gu": ("ફોટો ખૂબ ઘેરો છે ({v} ભાગ લગભગ કાળો છે). ઘેરો ફોટો પ્રિન્ટમાં વધુ ઘેરો આવે છે અને શેડોની ડિટેલ જતી રહે છે.", "ફોટો થોડો હળવો કરો (શેડો 10-20% ઉપર ઉઠાવો) અને પૂરું પ્રિન્ટ કરતા પહેલાં પ્રૂફ મંગાવો."),
 "hinglish": ("Photo bahut dark hai ({v} hissa lagbhag kala hai). Dark photo print me aur dark aati hai aur shadow ki detail chali jaati hai.", "Photo ko thoda halka karo (shadow 10-20% uthao) aur poora print karne se pehle proof mangwao.")},
"not_bitmap_gradient": {
 "en": ("Fountain colour (gradient) is left as vector. It can change or band at the printer.", "Convert gradients/effects to bitmap (300 dpi, CMYK) before exporting."),
 "hi": ("फ़ाउंटेन कलर (ग्रेडिएंट) वेक्टर में छोड़ा गया है। प्रिंटर पर यह बदल सकता है या पट्टियाँ आ सकती हैं।", "एक्सपोर्ट से पहले ग्रेडिएंट/इफ़ेक्ट को बिटमैप (300 dpi, CMYK) में बदलें।"),
 "gu": ("ફાઉન્ટન કલર (ગ્રેડિયન્ટ) વેક્ટરમાં રાખ્યો છે. પ્રિન્ટર પર તે બદલાઈ શકે અથવા પટ્ટા આવી શકે.", "એક્સપોર્ટ પહેલાં ગ્રેડિયન્ટ/ઇફેક્ટને બિટમેપ (300 dpi, CMYK) માં ફેરવો."),
 "hinglish": ("Fountain color (gradient) vector me chhoda hai. Printer pe ye badal sakta hai ya pattiyan aa sakti hain.", "Export se pehle gradient/effects ko bitmap (300 dpi, CMYK) me convert karo.")},
"not_bitmap_many": {
 "en": ("Too many separate elements on the page ({v}). The file can fail or change while processing for print.", "Convert the artwork (except text) to one bitmap (300 dpi, CMYK)."),
 "hi": ("पेज पर बहुत ज़्यादा अलग-अलग एलिमेंट हैं ({v})। प्रिंट के लिए प्रोसेस करते समय फ़ाइल अटक या बदल सकती है।", "टेक्स्ट को छोड़कर आर्टवर्क को एक बिटमैप (300 dpi, CMYK) में बदलें।"),
 "gu": ("પેજ પર ઘણા બધા અલગ એલિમેન્ટ છે ({v}). પ્રિન્ટ માટે પ્રોસેસ કરતી વખતે ફાઇલ અટકી કે બદલાઈ શકે.", "ટેક્સ્ટ સિવાયના આર્ટવર્કને એક બિટમેપ (300 dpi, CMYK) માં ફેરવો."),
 "hinglish": ("Page pe bahut zyada alag-alag elements hain ({v}). Print ke liye process karte time file atak ya badal sakti hai.", "Text ko chhod ke artwork ko ek bitmap (300 dpi, CMYK) me convert karo.")},
"page_seq_break": {
 "en": ("Page numbers do not follow in order ({v}). Please confirm the page sequence.", "Check the page order before printing."),
 "hi": ("पेज नंबर क्रम में नहीं हैं ({v})। कृपया पेज का क्रम पक्का करें।", "प्रिंट से पहले पेज का क्रम जाँचें।"),
 "gu": ("પેજ નંબર ક્રમમાં નથી ({v}). કૃપા કરી પેજનો ક્રમ પાકો કરો.", "પ્રિન્ટ પહેલાં પેજનો ક્રમ તપાસો."),
 "hinglish": ("Page number sequence me nahi hain ({v}). Page ka order confirm karo.", "Print se pehle page ka order check karo.")},
"page_seq_none": {
 "en": ("This file has {v} pages and no page numbers were found. Please confirm the page sequence.", "Check the page order before printing."),
 "hi": ("इस फ़ाइल में {v} पेज हैं और पेज नंबर नहीं मिले। कृपया पेज का क्रम पक्का करें।", "प्रिंट से पहले पेज का क्रम जाँचें।"),
 "gu": ("આ ફાઇલમાં {v} પેજ છે અને પેજ નંબર મળ્યા નથી. કૃપા કરી પેજનો ક્રમ પાકો કરો.", "પ્રિન્ટ પહેલાં પેજનો ક્રમ તપાસો."),
 "hinglish": ("Is file me {v} page hain aur page number nahi mile. Page ka order confirm karo.", "Print se pehle page ka order check karo.")},
"pages_not_x4": {
 "en": ("The file has {v} pages. A stitched book needs pages in multiples of 4. Please confirm.", "Add or remove pages if this is a centre-pin book."),
 "hi": ("फ़ाइल में {v} पेज हैं। पिन वाली किताब में पेज 4 के गुणा में चाहिए। कृपया पक्का करें।", "सेंटर पिन बुक हो तो पेज जोड़ें या घटाएँ।"),
 "gu": ("ફાઇલમાં {v} પેજ છે. પિનવાળી બુકમાં પેજ 4 ના ગુણાંકમાં જોઈએ. કૃપા કરી ખાતરી કરો.", "સેન્ટર પિન બુક હોય તો પેજ ઉમેરો કે ઘટાડો."),
 "hinglish": ("File me {v} page hain. Pin wali book me page 4 ke guna me chahiye. Confirm karo.", "Center pin book ho to page jodo ya ghatao.")},
"single_colour_mix": {
 "en": ("This is a single-colour job, but the design uses mixed colours ({v}).", "Keep the whole design in one colour only."),
 "hi": ("यह सिंगल कलर जॉब है, पर डिज़ाइन में मिक्स कलर हैं ({v})।", "पूरा डिज़ाइन सिर्फ़ एक ही कलर में रखें।"),
 "gu": ("આ સિંગલ કલર જોબ છે, પણ ડિઝાઇનમાં મિક્સ કલર છે ({v}).", "આખી ડિઝાઇન ફક્ત એક જ કલરમાં રાખો."),
 "hinglish": ("Ye single color job hai, par design me mix color hain ({v}).", "Poora design sirf ek hi color me rakho.")},
"mix_black": {
 "en": ("Black {v} is made from mixed CMYK instead of only K. It can look blurry or coloured at the edges.", "Use 100% K only (C0 M0 Y0 K100) for text and thin lines."),
 "hi": ("काला {v} सिर्फ़ K की जगह मिक्स CMYK से बना है। किनारों पर धुंधला या रंगीन दिख सकता है।", "टेक्स्ट और पतली लाइन में सिर्फ़ 100% K (C0 M0 Y0 K100) रखें।"),
 "gu": ("કાળો {v} ફક્ત K ને બદલે મિક્સ CMYK થી બન્યો છે. કિનારે ઝાંખો કે રંગીન દેખાઈ શકે.", "ટેક્સ્ટ અને પાતળી લાઇનમાં ફક્ત 100% K (C0 M0 Y0 K100) રાખો."),
 "hinglish": ("Black {v} sirf K ki jagah mix CMYK se bana hai. Kinaro pe blur ya rangeen dikh sakta hai.", "Text aur patli line me sirf 100% K (C0 M0 Y0 K100) rakho.")},
"light_design": {
 "en": ("The design is very light (darkest part is about {v}). It may hardly show in print.", "Make the colours darker if this is not meant to be a watermark."),
 "hi": ("डिज़ाइन बहुत हल्का है (सबसे गहरा हिस्सा लगभग {v})। प्रिंट में मुश्किल से दिखेगा।", "यह वॉटरमार्क न हो तो रंग गहरे करें।"),
 "gu": ("ડિઝાઇન ખૂબ હળવી છે (સૌથી ઘેરો ભાગ લગભગ {v}). પ્રિન્ટમાં ભાગ્યે જ દેખાશે.", "આ વોટરમાર્ક ન હોય તો રંગ ઘેરા કરો."),
 "hinglish": ("Design bahut light hai (sabse dark hissa lagbhag {v}). Print me mushkil se dikhega.", "Ye watermark nahi hai to color dark karo.")},
"dark_watermark": {
 "en": ("The watermark in the middle looks too dark (about {v}). Writing or printing on top of it will be hard to read.", "Make the watermark lighter (around 5-10%)."),
 "hi": ("बीच का वॉटरमार्क ज़्यादा गहरा लग रहा है (लगभग {v})। इसके ऊपर लिखा या छपा पढ़ना मुश्किल होगा।", "वॉटरमार्क हल्का करें (लगभग 5-10%)।"),
 "gu": ("વચ્ચેનો વોટરમાર્ક વધારે ઘેરો લાગે છે (લગભગ {v}). તેની ઉપર લખેલું કે છાપેલું વાંચવું મુશ્કેલ થશે.", "વોટરમાર્ક હળવો કરો (લગભગ 5-10%)."),
 "hinglish": ("Beech ka watermark zyada dark lag raha hai (lagbhag {v}). Iske upar likha ya chhapa padhna mushkil hoga.", "Watermark halka karo (lagbhag 5-10%).")},
"blank_page": {
 "en": ("This page is blank.", "Remove it if it is not needed."),
 "hi": ("यह पेज ख़ाली है।", "ज़रूरत न हो तो हटा दें।"),
 "gu": ("આ પેજ ખાલી છે.", "જરૂર ન હોય તો કાઢી નાખો."),
 "hinglish": ("Ye page khaali hai.", "Zaroorat nahi hai to hata do.")},
"border_near_edge": {
 "en": ("A border is only {v} from the cutting edge. If the cut shifts, the border will look uneven.", "Move the border at least {e} inside, or remove it."),
 "hi": ("बॉर्डर कटिंग किनारे से सिर्फ़ {v} दूर है। कटिंग हिली तो बॉर्डर टेढ़ा दिखेगा।", "बॉर्डर को कम से कम {e} अंदर करें, या हटा दें।"),
 "gu": ("બોર્ડર કટિંગ કિનારાથી ફક્ત {v} દૂર છે. કટિંગ ખસે તો બોર્ડર વાંકી દેખાશે.", "બોર્ડરને ઓછામાં ઓછી {e} અંદર કરો, અથવા કાઢી નાખો."),
 "hinglish": ("Border cutting kinare se sirf {v} door hai. Cutting hili to border tedha dikhega.", "Border ko kam se kam {e} andar karo, ya hata do.")},
"white_small_text": {
 "en": ("Small white text ({v}) on a dark background. Ink can fill it in and make it unreadable.", "Make the text bigger/bolder (at least {e})."),
 "hi": ("गहरे बैकग्राउंड पर छोटा सफ़ेद टेक्स्ट ({v})। इंक भरने से पढ़ना मुश्किल हो सकता है।", "टेक्स्ट बड़ा/मोटा करें (कम से कम {e})।"),
 "gu": ("ઘેરા બેકગ્રાઉન્ડ પર નાનું સફેદ ટેક્સ્ટ ({v}). ઇંક ભરાવાથી વાંચવું મુશ્કેલ થઈ શકે.", "ટેક્સ્ટ મોટું/જાડું કરો (ઓછામાં ઓછું {e})."),
 "hinglish": ("Dark background pe chhota safed text ({v}). Ink bharne se padhna mushkil ho sakta hai.", "Text bada/bold karo (kam se kam {e}).")},
"huge_image_skip": {
 "en": ("One image on this page is very high-resolution. Its size (dpi) was checked, but its colour and darkness could not be checked automatically.", "Please look at this image once yourself before printing."),
 "hi": ("इस पेज की एक इमेज बहुत हाई-रेज़ोल्यूशन है। उसका dpi चेक हो गया, पर रंग और गहराई अपने-आप चेक नहीं हो सकी।", "प्रिंट से पहले इस इमेज को खुद एक बार देख लें।"),
 "gu": ("આ પેજની એક ઇમેજ ખૂબ હાઈ-રિઝોલ્યુશન છે. તેનું dpi ચેક થયું, પણ રંગ અને ઘેરાપણું જાતે ચેક ન થઈ શક્યું.", "પ્રિન્ટ પહેલાં આ ઇમેજ જાતે એક વાર જોઈ લો."),
 "hinglish": ("Is page ki ek image bahut high-resolution hai. Uska dpi check ho gaya, par color aur darkness apne-aap check nahi ho saki.", "Print se pehle is image ko khud ek baar dekh lo.")},
"corrupt": {
 "en": ("This file could not be opened. It may be corrupt or password-protected.", "Export the file again and upload. Your credits are refunded."),
 "hi": ("यह फ़ाइल खुल नहीं सकी। यह खराब या पासवर्ड वाली हो सकती है।", "फ़ाइल दोबारा एक्सपोर्ट करके अपलोड करें। आपके क्रेडिट वापस हो गए हैं।"),
 "gu": ("આ ફાઇલ ખુલી શકી નહીં. તે બગડેલી અથવા પાસવર્ડવાળી હોઈ શકે.", "ફાઇલ ફરી એક્સપોર્ટ કરીને અપલોડ કરો. તમારા ક્રેડિટ પાછા આપ્યા છે."),
 "hinglish": ("Ye file khul nahi saki. Corrupt ya password wali ho sakti hai.", "File dobara export karke upload karo. Aapke credits wapas ho gaye.")},
"processing_failed": {
 "en": ("Something went wrong while checking this file (not a problem with your design).", "Please try uploading again. If it keeps happening, contact support@cleara.in. Your credits are refunded."),
 "hi": ("इस फ़ाइल को चेक करते समय कुछ गड़बड़ हो गई (आपकी डिज़ाइन में कोई समस्या नहीं है)।", "कृपया दोबारा अपलोड करें। अगर बार-बार हो तो support@cleara.in पर संपर्क करें। आपके क्रेडिट वापस हो गए हैं।"),
 "gu": ("આ ફાઇલ ચેક કરતી વખતે કંઈક ગરબડ થઈ (તમારી ડિઝાઇનમાં કોઈ સમસ્યા નથી).", "કૃપા કરી ફરી અપલોડ કરો. વારંવાર થાય તો support@cleara.in પર સંપર્ક કરો. તમારા ક્રેડિટ પાછા આપ્યા છે."),
 "hinglish": ("Is file ko check karte waqt kuch gadbad ho gayi (tumhari design mein koi problem nahi hai).", "Please dobara upload karo. Baar-baar ho to support@cleara.in par contact karo. Aapke credits wapas ho gaye.")},
}
LANGS = ["en", "hi", "gu", "hinglish"]

def build(code, v="", e=""):
    t = M[code]
    msg = {l: t[l][0].format(v=v, e=e) for l in LANGS}
    fix = {l: t[l][1].format(v=v, e=e) for l in LANGS}
    return msg, fix
