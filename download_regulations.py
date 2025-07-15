
#!/usr/bin/env python3
"""
Cannabis Regulation Download Script
Downloads regulations from all cannabis-legal states and organizes by state
"""

import os
import subprocess
import json
import logging
from datetime import datetime
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegulationDownloader:
    def __init__(self, base_dir: str = "regulations"):
        self.base_dir = base_dir
        self.state_urls = self._get_state_regulation_urls()
        
    def _get_state_regulation_urls(self) -> Dict[str, Dict[str, str]]:
        """Define URLs for each state's cannabis regulations"""
        return {
            "CO": {
                "name": "Colorado",
                "agency": "Marijuana Enforcement Division",
                "urls": [
                    "https://sbg.colorado.gov/sites/sbg/files/documents/1%20CCR%20212-3.pdf",
                    "https://leg.colorado.gov/sites/default/files/documents/2021A/bills/2021a_1090_signed.pdf"
                ]
            },
            "CA": {
                "name": "California", 
                "agency": "Department of Cannabis Control",
                "urls": [
                    "https://cannabis.ca.gov/wp-content/uploads/sites/2/2021/12/DCC_CommercialCannabisRegulations_2022.pdf",
                    "https://cannabis.ca.gov/wp-content/uploads/sites/2/2022/01/Medicinal_Cannabis_Regulations.pdf"
                ]
            },
            "WA": {
                "name": "Washington",
                "agency": "Liquor and Cannabis Board", 
                "urls": [
                    "https://lcb.wa.gov/sites/default/files/publications/rules/WAC-314-55.pdf",
                    "https://lcb.wa.gov/sites/default/files/publications/Marijuana/bulletins/FAQ-TRACEABILITY.pdf"
                ]
            },
            "OR": {
                "name": "Oregon",
                "agency": "Liquor and Cannabis Commission",
                "urls": [
                    "https://www.oregon.gov/olcc/marijuana/Documents/CTS/CTS_ManualCoverAndContents.pdf",
                    "https://www.oregon.gov/olcc/marijuana/Documents/Bulletins/2023/MB2023-05.pdf"
                ]
            },
            "AK": {
                "name": "Alaska",
                "agency": "Marijuana Control Board",
                "urls": [
                    "https://www.commerce.alaska.gov/web/Portals/9/pub/MCB/StatutesAndRegulations/3AAC306_MarijuanaControlBoard.pdf"
                ]
            },
            "AZ": {
                "name": "Arizona", 
                "agency": "Department of Health Services",
                "urls": [
                    "https://azdhs.gov/documents/licensing/medical-marijuana/rules/adult-use-marijuana-rules.pdf"
                ]
            },
            "CT": {
                "name": "Connecticut",
                "agency": "Department of Consumer Protection", 
                "urls": [
                    "https://portal.ct.gov/-/media/DCP/regulations/title_21/21-430-1_thru_21-430-81.pdf"
                ]
            },
            "DE": {
                "name": "Delaware",
                "agency": "Division of Alcohol and Tobacco Enforcement",
                "urls": [
                    "https://regs.delaware.gov/register/april2022/proposed/25%20DE%20Reg%201012%2004-01-22.pdf"
                ]
            },
            "IL": {
                "name": "Illinois",
                "agency": "Cannabis Control Board",
                "urls": [
                    "https://www2.illinois.gov/sites/agr/Plants/Documents/Hemp%20Program/Final%20Hemp%20Rules.pdf"
                ]
            },
            "ME": {
                "name": "Maine",
                "agency": "Office of Cannabis Policy",
                "urls": [
                    "https://www.maine.gov/dafs/ocp/sites/maine.gov.dafs.ocp/files/inline-files/Ch1AdultUseCannabisEstablishments.pdf"
                ]
            },
            "MD": {
                "name": "Maryland",
                "agency": "Cannabis Control Authority",
                "urls": [
                    "https://mmcc.maryland.gov/Documents/Patient%20and%20Caregiver%20Registry/FINAL%20COMAR%2010.62.30%20-%20Patient%20and%20Caregiver%20Registry%20Program.pdf"
                ]
            },
            "MA": {
                "name": "Massachusetts",
                "agency": "Cannabis Control Commission",
                "urls": [
                    "https://mass-cannabis-control.com/wp-content/uploads/2022/12/935_CMR_500.000_Adult_Use_of_Marijuana.pdf"
                ]
            },
            "MI": {
                "name": "Michigan",
                "agency": "Cannabis Regulatory Agency", 
                "urls": [
                    "https://www.michigan.gov/cra/-/media/Project/Websites/cra/documents/adult-use/R-420-1-R-420-75-Adult-Use-Marihuana-Rules.pdf"
                ]
            },
            "MO": {
                "name": "Missouri",
                "agency": "Division of Cannabis Regulation",
                "urls": [
                    "https://health.mo.gov/safety/medical-marijuana/pdf/19CSR30-95.pdf"
                ]
            },
            "MT": {
                "name": "Montana",
                "agency": "Cannabis Control Division",
                "urls": [
                    "https://mtrevenue.gov/wp-content/uploads/2022/01/Cannabis-Control-Division-Rules-42.39.101-42.39.501.pdf"
                ]
            },
            "NV": {
                "name": "Nevada", 
                "agency": "Cannabis Compliance Board",
                "urls": [
                    "https://ccb.nv.gov/wp-content/uploads/2021/07/NAC-453D-Adult-Use-Cannabis.pdf"
                ]
            },
            "NJ": {
                "name": "New Jersey",
                "agency": "Cannabis Regulatory Commission",
                "urls": [
                    "https://www.nj.gov/cannabis/documents/rules/personal-use-cannabis-rules.pdf"
                ]
            },
            "NM": {
                "name": "New Mexico",
                "agency": "Regulation and Licensing Department",
                "urls": [
                    "https://www.rld.nm.gov/uploads/files/16.8.2%20NMAC%20Cannabis%20Control%20Act%20Rules.pdf"
                ]
            },
            "NY": {
                "name": "New York", 
                "agency": "Office of Cannabis Management",
                "urls": [
                    "https://cannabis.ny.gov/system/files/documents/2022/10/part-116-adult-use-cannabis-regulations.pdf"
                ]
            },
            "RI": {
                "name": "Rhode Island",
                "agency": "Department of Business Regulation",
                "urls": [
                    "https://dbr.ri.gov/documents/regulations/DBR-Cannabis-Regulations.pdf"
                ]
            },
            "VT": {
                "name": "Vermont",
                "agency": "Cannabis Control Board", 
                "urls": [
                    "https://ccb.vermont.gov/sites/ccb/files/documents/Rules/CCB%20Rule%201%20-%20Licensing%20-%20ADOPTED%202023-01-11.pdf"
                ]
            },
            "VA": {
                "name": "Virginia",
                "agency": "Cannabis Control Authority",
                "urls": [
                    "https://www.vacannabiscontrolauthority.com/sites/default/files/2022-12/1VAC5-10%20Cannabis%20Control%20Authority%20Regulations.pdf"
                ]
            },
            "FL": {
                "name": "Florida (Medical Only)",
                "agency": "Department of Health",
                "urls": [
                    "https://www.flrules.org/gateway/ruleNo.asp?id=64-4.001"
                ]
            },
            "OH": {
                "name": "Ohio (Medical Only)",
                "agency": "Department of Commerce",
                "urls": [
                    "https://www.com.ohio.gov/documents/dico_MedicalMarijuanaControlProgramRules.pdf"
                ]
            },
            "PA": {
                "name": "Pennsylvania (Medical Only)", 
                "agency": "Department of Health",
                "urls": [
                    "https://www.health.pa.gov/topics/Documents/Programs/Medical%20Marijuana/DOH%20Medical%20Marijuana%20Regulations.pdf"
                ]
            }
        }
    
    def create_state_directory(self, state_code: str) -> str:
        """Create directory for state regulations"""
        state_dir = os.path.join(self.base_dir, state_code)
        os.makedirs(state_dir, exist_ok=True)
        return state_dir
    
    def download_state_regulations(self, state_code: str) -> bool:
        """Download all regulations for a specific state"""
        if state_code not in self.state_urls:
            logger.error(f"Unknown state code: {state_code}")
            return False
            
        state_info = self.state_urls[state_code]
        state_dir = self.create_state_directory(state_code)
        
        logger.info(f"Downloading regulations for {state_info['name']} ({state_code})")
        
        success = True
        for i, url in enumerate(state_info['urls']):
            try:
                # Generate filename from URL
                filename = f"{state_code}_regulation_{i+1}.pdf"
                filepath = os.path.join(state_dir, filename)
                
                # Use wget to download
                cmd = [
                    'wget', 
                    '--timeout=30',
                    '--tries=3', 
                    '--user-agent=Mozilla/5.0 (compatible; ComplianceBot/1.0)',
                    '-O', filepath,
                    url
                ]
                
                logger.info(f"Downloading: {url}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Successfully downloaded: {filename}")
                else:
                    logger.error(f"Failed to download {url}: {result.stderr}")
                    success = False
                    
            except Exception as e:
                logger.error(f"Error downloading {url}: {str(e)}")
                success = False
        
        # Create metadata file
        metadata = {
            "state": state_code,
            "name": state_info['name'],
            "agency": state_info['agency'],
            "last_updated": datetime.now().isoformat(),
            "urls": state_info['urls'],
            "download_success": success
        }
        
        metadata_path = os.path.join(state_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return success
    
    def download_all_regulations(self) -> Dict[str, bool]:
        """Download regulations for all states"""
        logger.info("Starting download of all state regulations")
        
        # Create base directory
        os.makedirs(self.base_dir, exist_ok=True)
        
        results = {}
        for state_code in self.state_urls.keys():
            results[state_code] = self.download_state_regulations(state_code)
            
        # Create summary report
        summary = {
            "download_date": datetime.now().isoformat(),
            "total_states": len(self.state_urls),
            "successful_downloads": sum(results.values()),
            "failed_downloads": len(self.state_urls) - sum(results.values()),
            "results": results
        }
        
        summary_path = os.path.join(self.base_dir, 'download_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        logger.info(f"Download complete. Success: {summary['successful_downloads']}/{summary['total_states']}")
        return results

def main():
    """Main function to run the downloader"""
    downloader = RegulationDownloader()
    results = downloader.download_all_regulations()
    
    # Print summary
    successful = sum(results.values())
    total = len(results)
    print(f"\n📊 Download Summary:")
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful < total:
        print("\n⚠️  Failed downloads:")
        for state, success in results.items():
            if not success:
                print(f"   - {state}")

if __name__ == "__main__":
    main()
