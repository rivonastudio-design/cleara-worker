# Messages for every finding code in 4 languages. {v}=found value, {e}=expected value
M = {
"bleed_missing": {
 "en": ("Bleed is {v}, needs {e}. Bleed is the extra design that goes past the cutting line. Without it a white strip can show on the edge after cutting.", "Extend the background/photo {e} beyond the cutting line on every side and export again."),
 "hi": ("ब्लीड {v} है, {e} चाहिए। ब्लीड यानी कटिंग लाइन के बाहर तक जाने वाला एक्स्ट्रा डिज़ाइन। इसके बिना कटिंग के बाद किनारे पर सफ़ेद पट्टी दिख सकती है।", "बैकग्राउंड/फ़ोटो को हर तरफ़ कटिंग लाइन से {e} बाहर तक बढ़ाएँ और दोबारा एक्सपोर्ट करें।"),
 "gu": ("બ્લીડ {v} છે, {e} જોઈએ. બ્લીડ એટલે કટિંગ લાઇનની બહાર સુધી જતી વધારાની ડિઝાઇન. તેના વગર કટિંગ પછી કિનારે સફેદ પટ્ટી દેખાઈ શકે.", "બેકગ્રાઉન્ડ/ફોટોને દરેક બાજુ કટિંગ લાઇનથી {e} બહાર સુધી વધારો અને ફરી એક્સપોર્ટ કરો."),
 "hinglish": ("Bleed {v} hai, {e} chahiye. Bleed matlab cutting line ke bahar tak jaane wala extra design. Iske bina cutting ke baad kinare pe safed patti dikh sakti hai.", "Background/photo ko har taraf cutting line se {e} bahar tak badhao aur dobara export karo.")},
"bleed_unknown": {
 "en": ("The design touches the edge, but the file does not say where the cutting line is. Please confirm bleed (extra design past the cutting line) is included.", "Check that the background goes 3 mm past the cutting line on every side."),
 "hi": ("डिज़ाइन किनारे तक है, पर फ़ाइल में कटिंग लाइन की जानकारी नहीं है। कृपया पुष्टि करें कि ब्लीड (कटिंग लाइन के बाहर का एक्स्ट्रा डिज़ाइन) शामिल है।", "जाँचें कि बैकग्राउंड हर तरफ़ कटिंग लाइन से 3 मिमी बाहर तक है।"),
 "gu": ("ડિઝાઇન કિનારા સુધી છે, પણ ફાઇલમાં કટિંગ લાઇનની માહિતી નથી. કૃપા કરી ખાતરી કરો કે બ્લીડ (કટિંગ લાઇનની બહારની વધારાની ડિઝાઇન) શામેલ છે.", "તપાસો કે બેકગ્રાઉન્ડ દરેક બાજુ કટિંગ લાઇનથી 3 મિમી બહાર સુધી છે."),
 "hinglish": ("Design kinare tak hai, par file me cutting line ki jaankari nahi hai. Confirm karo ki bleed (cutting line ke bahar ka extra design) rakha hai.", "Check karo ki background har taraf cutting line se 3 mm bahar tak hai.")},
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
 "en": ("Image resolution is {v} (needs {e}). It will print blurry.", "Use a higher-resolution original image."),
 "hi": ("इमेज रेज़ोल्यूशन {v} है ({e} चाहिए)। प्रिंट धुंधला आएगा।", "ज़्यादा रेज़ोल्यूशन वाली ओरिजिनल इमेज इस्तेमाल करें।"),
 "gu": ("ઇમેજ રિઝોલ્યુશન {v} છે ({e} જોઈએ). પ્રિન્ટ ઝાંખું આવશે.", "વધુ રિઝોલ્યુશનવાળી મૂળ ઇમેજ વાપરો."),
 "hinglish": ("Image resolution {v} hai ({e} chahiye). Print blur aayega.", "Zyada resolution wali original image use karo.")},
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
"hairline": {
 "en": ("Line is {v} thick, thinner than {e}. May not print.", "Make the line at least 0.25 pt."),
 "hi": ("लाइन {v} मोटी है, {e} से पतली। प्रिंट न हो सकती है।", "लाइन कम से कम 0.25 pt रखें।"),
 "gu": ("લાઇન {v} જાડી છે, {e} કરતાં પાતળી. પ્રિન્ટ ન થઈ શકે.", "લાઇન ઓછામાં ઓછી 0.25 pt રાખો."),
 "hinglish": ("Line {v} moti hai, {e} se patli. Print na ho sakti hai.", "Line kam se kam 0.25 pt rakho.")},
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
"size_mismatch": {
 "en": ("File size is {v}, but the selected size is {e}.", "Resize the artwork to the selected size."),
 "hi": ("फ़ाइल साइज़ {v} है, पर चुना हुआ साइज़ {e} है।", "आर्टवर्क को चुने हुए साइज़ में बदलें।"),
 "gu": ("ફાઇલ સાઇઝ {v} છે, પણ પસંદ કરેલું સાઇઝ {e} છે.", "આર્ટવર્કને પસંદ કરેલા સાઇઝમાં બદલો."),
 "hinglish": ("File size {v} hai, par chuna hua size {e} hai.", "Artwork ko chuni hui size me badlo.")},
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
"corrupt": {
 "en": ("This file could not be opened. It may be corrupt or password-protected.", "Export the file again and upload. Your credits are refunded."),
 "hi": ("यह फ़ाइल खुल नहीं सकी। यह खराब या पासवर्ड वाली हो सकती है।", "फ़ाइल दोबारा एक्सपोर्ट करके अपलोड करें। आपके क्रेडिट वापस हो गए हैं।"),
 "gu": ("આ ફાઇલ ખુલી શકી નહીં. તે બગડેલી અથવા પાસવર્ડવાળી હોઈ શકે.", "ફાઇલ ફરી એક્સપોર્ટ કરીને અપલોડ કરો. તમારા ક્રેડિટ પાછા આપ્યા છે."),
 "hinglish": ("Ye file khul nahi saki. Corrupt ya password wali ho sakti hai.", "File dobara export karke upload karo. Aapke credits wapas ho gaye.")},
}
LANGS = ["en", "hi", "gu", "hinglish"]

def build(code, v="", e=""):
    t = M[code]
    msg = {l: t[l][0].format(v=v, e=e) for l in LANGS}
    fix = {l: t[l][1].format(v=v, e=e) for l in LANGS}
    return msg, fix
