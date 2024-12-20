
from flask import Flask, make_response
#from nonce_tool import NonceTool

class GetInfoForm:

    def __init__(self):

        #self.nonce = NonceTool.generate_nonce()
        self.nonce = 'hello'

    def main(self):

        html_form = f"""
            <h2>Hi, I am ConcuAid</h2>
            <h4>I am so happy to be able to help you in all of your questions about concussion prevention and treatment.</h4>
            <form method="post" action="">
                 <div class="small" style="margin-top:10px;margin-bottom:10px">
                    <h5 style="color:red;font-weight:bold;">Disclaimer:</h5>
                    ConcuAid is an AI assistant designed to provide general information and support for concussion awareness and recovery. 
                    It <span style="font-weight:bold">is not a substitute for professional medical advice, diagnosis, or treatment</span>. If you suspect that you or someone else 
                    may have a concussion, please consult a licensed medical professional immediately. Always seek the guidance of your doctor 
                    or other qualified health providers with any questions you may have regarding a medical condition.
                </div>
                <table class="form-table">
                    <tr>
                        <td rowspan="99">
                            <img id="rotating-image" src="/wp-content/uploads/2024/12/cropped-artificial-intelligence-icon-1.webp" style="heigth:33%;weigth:33%" alt="Rotating Image">
                        </td>
                        <th scope="row">
                            <label for="job_id">What do you want</label>
                        </th>
                        <td style="width:75%;">
                            <select name="what" id="what" required>
                                <option value="">-- Select an Action --</option>
                                <option value="Ask Question">Ask a Question</option>
                                <option value="Ask Paragraph">Write Paragraph</option>
                                <option value="Ask Accuracy">Check Accuracy</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row" valign="top">
                            <label for="resume_id">Text</label>
                        </th>
                        <td>
                            <textarea name='text' id='text' playholder='Enter your text'></textarea>
                        </td>
                    </tr>
                </table>
                <input type="button" id="generate-llm-response" value="Generate Response" style="margin-top:10px;margin-bottom:10px"/>
                <div id='concuaid_response'>
            </form>
        """

        html_css = """"""
        
        html_content = html_form + html_css
        # Create a response object and set the correct content type
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'  # Ensure the content is treated as HTML
        return response