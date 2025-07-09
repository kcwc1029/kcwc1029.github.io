
keyword：self-assessment accuracy (SAA)

## 1. 摘要

- 反饋(Feedback)是一種很有前途的干預措施，可以提高學生的自我評估準確性(self-assessment accuracy, SSA)

### 1.1. 研究目標

為了加深我們的理解 (To deepen our understanding)，本研究探討了反饋(Feedback)與自我評估準確性(self-assessment accuracy, SSA)之間的機制與結果。
- 變數：在隨機對照實驗中，我們通過將學生的初始表現和初始 SAA 視為潛在的調節因素，檢查了 LLM 生成的反饋對 SAA 的影響。 
- 研究流程：樣本 N = 459 名高中生用英語作為外語寫了一篇議論文，並修改了他們的文本。在完成草稿的初稿（預測）和修訂（後測）后，學生們自我評估了他們的寫作表現。
	- 實驗組的學生在複習期間收到了 GPT-3.5-turbo 生成的關於他們初稿的反饋。
	- 對照組中，學生可以在沒有反饋的情況下修改他們的文本。

## 2. Introduction

隨著人工智慧（Artificial Intelligence, AI）於教育領域中扮演日益關鍵的角色，技術導向的學習模式不僅重塑學習方法，更成為促進知識建構與創新應用的核心策略（Lan & Zhou, 2025）。為了在變動快速且自主性高度要求的環境中獲致良好學習成效，學生需展現高度的自我調節學習（Self-Regulated Learning, SRL）能力。包含有效的時間與資源管理、個別學習目標的設定，以及對策略與進度之持續性監控與評估（Chang et al., 2023）

自我評估準確性（Self-Assessment Accuracy, SAA）被描述為學生對自身表現的評估與實際表現之間的一致程度(Wang et al., 2025)。然而Panadero et al.（2016）指出，多數學生傾向高估自身表現，導致評估結果偏誤，難以據以調整學習策略。這促使研究呼籲採取有效的干預措施以提升學生的SAA（Lan & Zhou, 2025）。

提供具針對性的反饋（Feedback）為一項被廣泛證實有效的干預措施，有助於促進學生對任務要求與表現標準的理解，進而提高其自我評估的準確性（Braumann et al., 2024）。表現較差的學生在SAA上通常落後於同儕，因而更需依賴教師或AI系統提供的回饋訊息，這些學生透過具體與即時的回饋，可獲得學習方向上的明確指引，有效修正錯誤認知並調整策略，從而促進其學習動力與元認知發展（Liu et al., 2025）。

對於教師而言，提供反饋是一項極具挑戰性的任務，尤其針對複雜的寫作任務等涵蓋極高的時間與認知成本（Liebenow et al., 2025）。隨著大型語言模型（Large Language Models, LLMs）的迅速發展，AI展現強化教學回饋的潛力，不僅能為大量學生提供即時、個人化的意見，也有助於減輕教師負擔並提升回饋覆蓋率。例如Meyer et al.,(2024)證明GPT 生成的回饋對學習成果具有正向影響，像是寫作表現、動機與情緒狀態的提升。然而，LLM 所生成之回饋是否能有效支持學生的自我評估準確性（Self-Assessment Accuracy, SAA）仍未獲得一致性證據。雖然AI可以提供快速且一致的回饋，但回饋在準確性、適切性與認知支持層面，與人類教師仍存在顯著差異（Liebenow et al., 2025）。例如AI 所生成的回饋可能缺乏情境敏感性，對於策略引導與錯誤識別的深度仍有待提升，進而影響其對 SAA 的潛在成效 。Lew et al.,(2010)則指出，提供明確績效標準或具結構性的反饋對學生的 SAA 提升尤為關鍵，尤其是針對初始表現較差之學生，績效導向的回饋能協助其重構自我理解與策略認知。

因此，本研究旨在探討LLM 生成的回饋是否能如同傳統人類教師回饋般有效促進學生的 SAA。透過隨機對照實驗設計，檢視學生在接收 GPT 生成之回饋後 SAA 的變化趨勢與學習績效之關聯。為了探究 AI 回饋對不同學生群體的影響，研究亦納入學生初始表現與原始 SAA 表現作為調節變項，旨在驗證研究核心假設：對於在自我監控與自我評估能力上相對薄弱的學生而言，結構化的外部回饋能發揮補償性作用，進而促進其學習調整與策略修正。

> 白話意思：
> 這份研究的目的是想了解，LLM所給的回饋，是否能向老師一樣，有助於學生更準確地評估自己SAA？
> 
> 進一步，研究想探討，不同學生會不會對 AI 回饋有不同的反應？
> 我們加入以下兩個變數：(1)學生初始表現。(2)學生原本的 SAA 準不準

本研究具體問題如下：
RQ1：LLM 生成的反饋是否能提高學生的 SAA？(Does LLM-generated feedback enhance students' SAA?)
RQ2：反饋是否根據學生的表現和 SAA 水平產生不同的影響？(Does feedback have differential effects depending on students' performance and SAA levels?)
RQ2a：與表現較高的學生相比，表現較差的學生可以通過 LLM 生成的反饋更好地提高他們的 SAA？(Lower-performing students can improve their SAA more with LLM-generated feedback compared to higher-performing students.)
RQ2b：與 SAA 較高的學生相比，SAA 較低的學生通過 LLM 生成的反饋更多地提高他們的 SAA？(Students with lower SAA improve their SAA more with LLM-generated feedback compared to students with higher SAA.)



Luo, R. Z., & Zhou, Y. L. (2024). The effectiveness of self‐regulated learning strategies in higher education blended learning: A five years systematic review. _Journal of Computer Assisted Learning_, _40_(6), 3005-3029.

Liebenow, L. W., Schmidt, F. T., Meyer, J., Panadero, E., Fleckenstein, J., & Education, S. P. S. C. Supporting Self-Assessment: A Systematic Review and Meta-Analysis of Feedback Effects.

Meyer, J., Jansen, T., Schiller, R., Liebenow, L. W., Steinbach, M., Horbach, A., & Fleckenstein, J. (2024). Using LLMs to bring evidence-based feedback into the classroom: AI-generated feedback increases secondary students’ text revision, motivation, and positive emotions. _Computers and Education: Artificial Intelligence_, _6_, 100199.

Panadero, E., Brown, G. T., & Strijbos, J. W. (2016). The future of student self-assessment: A review of known unknowns and potential directions. Educational psychology review, 28, 803-830.

Braumann, S., van de Pol, J., Kok, E., Pijeira-Díaz, H. J., van Wermeskerken, M., de Bruin, A. B., & van Gog, T. (2024). The role of feedback on students’ diagramming: Effects on monitoring accuracy and text comprehension. _Contemporary Educational Psychology_, _76_, 102251.

Chang, D. H., Lin, M. P. C., Hajian, S., & Wang, Q. Q. (2023). Educational design principles of using AI chatbot that supports self-regulated learning in education: Goal setting, feedback, and personalization. _Sustainability_, _15_(17), 12921.

Wang, W. S., Lin, C. J., Lee, H. Y., Huang, Y. M., & Wu, T. T. (2025). Enhancing self-regulated learning and higher-order thinking skills in virtual reality: the impact of ChatGPT-integrated feedback aids. _Education and Information Technologies_, 1-27.

Liu, C. C., Hwang, G. J., Yu, P., Tu, Y. F., & Wang, Y. (2025). Effects of an automated corrective feedback-based peer assessment approach on students’ learning achievement, motivation, and self-regulated learning conceptions in foreign language pronunciation. _Educational technology research and development_, 1-22.

Liebenow, L. W., Schmidt, F. T., Meyer, J., & Fleckenstein, J. (2025). Self-Assessment Accuracy in the Age of Artificial Intelligence: Differential Effects of LLM-Generated Feedback. _Computers & Education_, 105385.

Lew, M. D., Alwis, W. A. M., & Schmidt, H. G. (2010). Accuracy of students' self‐assessment and their beliefs about its utility. _Assessment & Evaluation in Higher Education_, _35_(2), 135-156.


## 3. 文獻探討：Self-assessment accuracy
自我評估（Self-assessment）涵蓋不同的技術與方式，協助學生自我監控學習歷程並判斷學習表現，進而促進學習調整與成效提升（Yan & Brown, 2017）。自我評估準確性（Self-assessment accuracy, SAA）SAA又被稱為校準精確度(calibration accuracy)（Hacker & Bol, 2019）或元認知監控準確性(metacognitive monitoring accuracy)（de Bruin & van Merriënboer, 2017），描述學生自我評估表與自身實際表現結果相對應的程度。

SAA 的研究受自我調節學習理論（Self-Regulated Learning, SRL）影響，被視為元認知歷程中的關鍵組成。學生若能準確評估自身學習狀態，更能設定合理目標、精準監測進展，並針對學習策略做出有效調整（Rickey et al., 2025）。而自我評估活動本身亦已被證實能提升學生的反思能力與自我監控意識，是培養SRL技能的重要歷程之一（Andrade, 2019）。Ernst et al.,(2025)則指出高準確度的 SAA 能促進學生對自身學習過程的現實理解，有助於減少過度自信或錯誤判斷所導致的策略失誤，提升學習效能與動機。

隨著自我評估準確性（Self-Assessment Accuracy, SAA）在自我調節學習歷程中的地位日益受到關注，自我評估與學術表現之間的關聯性也愈加明確。具備較高 SAA 的學生，能更現實地理解自身學習狀況，做出策略性調整，提升整體學習成效（Ernst et al., 2025）。這種能力使學生得以識別其學習中的知識盲區，並針對性地投入更多資源進行補強。Thiede et al.（2010）在文本理解領域的研究指出，SAA 較高的學生更能有效辨識需要重新學習的內容，並因此表現出更佳的學習成果。凸顯 SAA 不僅是一項元認知指標，更是實現有效學習的必要條件。

Hacker, D. J., & Bol, L. (2019). Calibration and self-regulated learning: Making the connections.

de Bruin, A. B., & van Merriënboer, J. J. (2017). Bridging cognitive load and self-regulated learning research: A complementary approach to contemporary issues in educational research. _Learning and Instruction_, _51_, 1-9.

Yan, Z., & Brown, G. T. (2017). A cyclical self-assessment process: Towards a model of how students engage in self-assessment. Assessment & Evaluation in Higher Education, 42(8), 1247-1262.

Rickey, N., Panadero, E., & DeLuca, C. (2025). How do students self-assess? examining the metacognitive processes of student self-assessment. _Metacognition and Learning_, _20_(1), 1-29.

Andrade, H. L. (2019, August). A critical review of research on student self-assessment. In _Frontiers in education_ (Vol. 4, p. 87). Frontiers Media SA.

Ernst, H. M., Prinz-Weiß, A., Wittwer, J., & Voss, T. (2025). Discrepancy between performance and feedback affects mathematics student teachers’ self-efficacy but not their self-assessment accuracy. _Frontiers in Psychology_, _15_, 1391093.

Thiede, K. W., Griffin, T. D., Wiley, J., & Anderson, M. C. (2010). Poor metacomprehension accuracy as a result of inappropriate cue use. _Discourse Processes_, _47_(4), 331-362.

Ernst, H. M., Prinz-Weiß, A., Wittwer, J., & Voss, T. (2025). Discrepancy between performance and feedback affects mathematics student teachers’ self-efficacy but not their self-assessment accuracy. _Frontiers in Psychology_, _15_, 1391093.

## 4. 文獻探討：Self-assessment accuracy and feedback(還沒寫完)

> 備註：
> 請老師幫忙下載文獻，裡面好像有一個框架
> 原paper：https://doi.org/10.1016/j.compedu.2025.105385
> 好像有框架的paper：https://psycnet.apa.org/doiLanding?doi=10.1037%2F0096-3445.126.4.349

León et al.,(2023)經查經常觀察到學生在自我評估中容易出現不準確，也強調了有效干預措施來支持學生 SAA 的必要性。這種現象可以通過提示利用框架來闡明(補充文獻)。



(未修飾)



León, S. P., Panadero, E., & García-Martínez, I. (2023). How accurate are our students? A meta-analytic systematic review on self-assessment scoring accuracy. _Educational Psychology Review_, _35_(4), 1

## 5. 文獻探討：Differential effects of feedback
學生本身的學業表現水準往往扮演關鍵調節角色。表現較差的學生通常傾向使用較為片面或無效的線索來進行自我評估，例如依賴任務完成的感覺而非具體目標達成情況，這可能源自其對任務結構的不熟悉與認知資源的受限（Kuklick et al., 2023）。然而，低表現學生的潛在受益空間也相對更大。相較於高表現學生，表現較差者在接受回饋後更有可能調整其元認知監控與學習策略，並展現更顯著的SAA提升（Huang et al., 2022）。此外，低表現學生亦被觀察到更頻繁地尋求與使用回饋，這可能反映其對學習方向的不確定性與對外部支援的高度依賴（Händel et al., 2020）。

儘管如此，關於表現水準與回饋效應之間交互作用的研究仍相對稀少。過往研究多忽視一項重要變項：SAA本身亦可能成為回饋效應的調節因子。若學生初始SAA較低，代表其在校準與監控上存在明顯困難，此時所接收的結構化回饋可作為校準參照點，有助於其辨識落差並進行策略性修正(Ernst et al., 2025)。這亦呼應了診斷性回饋（diagnostic feedback）在支持高風險學習者自我監控與調節中的核心作用。探討學生的初始表現與SAA水平如何共同調節回饋效應，不僅有助於釐清回饋機制運作之精細路徑，亦對高等教育中個別化教學介入設計具實質啟發意義。

Kuklick, L., Greiff, S., & Lindner, M. A. (2023). Computer-based performance feedback: Effects of error message complexity on cognitive, metacognitive, and motivational outcomes. Computers & Education, 200, 104785.

Huang, X., Bernacki, M. L., Kim, D., & Hong, W. (2022). Examining the role of self-efficacy and online metacognitive monitoring behaviors in undergraduate life science education. _Learning and Instruction_, _80_, 101577.

Händel, M., Harder, B., & Dresel, M. (2020). Enhanced monitoring accuracy and test performance: Incremental effects of judgment training over and above repeated testing. _Learning and Instruction_, _65_, 101245.

Ernst, H. M., Prinz-Weiß, A., Wittwer, J., & Voss, T. (2025). Discrepancy between performance and feedback affects mathematics student teachers’ self-efficacy but not their self-assessment accuracy. _Frontiers in Psychology_, _15_, 1391093.