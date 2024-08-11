from langchain_core.prompts.prompt import PromptTemplate
from cpeParser import CPEParser
from langchain_core.prompts.prompt import PromptTemplate

def create_prompt_template():
    return PromptTemplate(
        input_variables=["cve_id", "description"],
        template="""
        CPE (Common Platform Enumeration) is a unique identifier for information technology systems, software and packages. CPE facilitates the identification and matching of products and components. 
        This standard is used to more effectively perform vulnerabilities and configuration management of systems.
        CVE (Common Vulnerabilities and Exposures) is a unique identifier system that identifies security vulnerabilities found in software and hardware products. CVE numbers identify specific vulnerabilities and provide detailed information about them.
        CPE (Common Platform Enumeration) records help standardize the identification of security vulnerabilities and products. The key components that form CPE records are:
        Vendor: The manufacturer or provider of the product.
        Product: The name of the product.
        Version: A specific version of the product.
        Update: Updates or patch levels of the product.
        Edition: A particular edition or variant of the product (e.g., Professional, Enterprise).
        Language: indicates the language of the product. This indicates the language in which the product is available. For example, "en" (), "fr" (French).
        sw_edition: indicates a specific storage or capacity of the storage. This allows you to distribute different versions of the product. For example, "Home", "Business".
        target_sw: is the software platform or environment that the product is targeted to. For example, "Windows", "Linux".
        target_hw: is the hardware platform or environment that the product is targeted to. For example, "x86", "ARM".
        Other: Contains other identifying information. This may be additional information or features that do not fit into the categories.

        Given the following CVE (Common Vulnerabilities and Exposures) information, generate a list of CPE (Common Platform Enumeration) strings in the format:
        cpe:2.3:<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>:<sw_edition>:<target_sw>:<target_hw>:<other>
        
        CVE ID: {cve_id}
        Description: {description}
        
        Rules:
        1. Product type:
            - If software `a`
            - If hardware `h`
            - If operating system `o`     
        2. If there is a " " between words, you must put a "_" sign.
        3. All words must be in lower case.
        4. Use '*' for any field you cannot determine.
        5. Base your decision on the information provided in the description.
        6. Add to the list for the cpe that can be detected in the cpe list specified in the description. More than one cpe record can be detected. For example, there can be more than one version. For such operations, each structure should be checked and a list should be created. A cpe can also be detected, in which case the list should contain a single element.        
        7. If concepts such as before or all or through or prior to are used, the versions it contains must be given one by one in the cpe record.
        8. The same record should not be entered more than once.
        9. If a single cpe record is detected, it should return a single record
        10. If an expression that specifies more than one version is used when determining versions (e.g. all, before, more than, below, higher, lower etc.), all versions up to that version must be created in the cpe record.
        
        Provide ONLY the list of CPE strings as a JSON object. Do not include any explanations or additional text.
                The output should be a valid JSON object with a single key "cpe" whose value is an array of CPE strings.
        For each CVE ID and description, only the CPE value(s) should be generated.
                Each CPE should be included in the list within a single JSON; separate JSONs should not be created.

        Example:


        note: CVE_ID ve Description should not be in the output
        The model should derive the cpe result from these cve values. It should not print cve id and description.

        
        CVE_ID: "CVE-2018-1000843"
        Description: "Luigi version prior to version 2.8.0; after commit 53b52e12745075a8acc016d33945d9d6a7a6aaeb; after GitHub PR spotify/luigi/pull/1870 contains a Cross ite Request Forgery (CSRF) vulnerability in API endpoint: /api/<method> that can result in Task metadata such as task name, id, parameter, etc. will be leaked to unauthorized users. This attack appear to be exploitable via The victim must visit a specially crafted webpage from the network where their Luigi server is accessible.. This vulnerability appears to have been fixed in 2.8.0 and later."
        {{
        "cpe": [
        "cpe:2.3:a:spotify:luigi:1.0.16:*:*:*:*:*:*:*",
        "cpe:2.3:a:spotify:luigi:1.0.17:*:*:*:*:*:*:*",
        "cpe:2.3:a:spotify:luigi:1.3.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:spotify:luigi:2.7.9:*:*:*:*:*:*:*"
        ]
        }}

        important: 
         No comma after the last element of the list

        Generate the CPE list based on the given CVE information
        """
    )
