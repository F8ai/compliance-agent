
#!/usr/bin/env python3
"""
Cannabis Regulation Website Mirror Script
Downloads complete regulatory websites from all cannabis-legal states
"""

import os
import subprocess
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegulationMirror:
    def __init__(self, base_dir: str = "regulations"):
        self.base_dir = base_dir
        self.state_sites = self._get_state_regulatory_sites()
        
    def _get_state_regulatory_sites(self) -> Dict[str, Dict[str, str]]:
        """Define main regulatory websites for each state"""
        return {
            "CO": {
                "name": "Colorado",
                "agency": "Marijuana Enforcement Division",
                "main_url": "https://sbg.colorado.gov/med-enforcement",
                "mirror_domains": [
                    "sbg.colorado.gov/med-enforcement",
                    "leg.colorado.gov/bills/cannabis"
                ]
            },
            "CA": {
                "name": "California", 
                "agency": "Department of Cannabis Control",
                "main_url": "https://cannabis.ca.gov",
                "mirror_domains": [
                    "cannabis.ca.gov"
                ]
            },
            "WA": {
                "name": "Washington",
                "agency": "Liquor and Cannabis Board", 
                "main_url": "https://lcb.wa.gov/cannabis",
                "mirror_domains": [
                    "lcb.wa.gov/cannabis"
                ]
            },
            "OR": {
                "name": "Oregon",
                "agency": "Liquor and Cannabis Commission",
                "main_url": "https://www.oregon.gov/olcc/marijuana",
                "mirror_domains": [
                    "oregon.gov/olcc/marijuana"
                ]
            },
            "AK": {
                "name": "Alaska",
                "agency": "Marijuana Control Board",
                "main_url": "https://www.commerce.alaska.gov/web/amco",
                "mirror_domains": [
                    "commerce.alaska.gov/web/amco"
                ]
            },
            "AZ": {
                "name": "Arizona", 
                "agency": "Department of Health Services",
                "main_url": "https://azdhs.gov/licensing/medical-marijuana",
                "mirror_domains": [
                    "azdhs.gov/licensing/medical-marijuana"
                ]
            },
            "CT": {
                "name": "Connecticut",
                "agency": "Department of Consumer Protection", 
                "main_url": "https://portal.ct.gov/DCP/Drug-Control-Division/Drug-Control-Division",
                "mirror_domains": [
                    "portal.ct.gov/DCP/Drug-Control-Division"
                ]
            },
            "DE": {
                "name": "Delaware",
                "agency": "Division of Alcohol and Tobacco Enforcement",
                "main_url": "https://regs.delaware.gov",
                "mirror_domains": [
                    "regs.delaware.gov"
                ]
            },
            "IL": {
                "name": "Illinois",
                "agency": "Cannabis Control Board",
                "main_url": "https://www2.illinois.gov/sites/agr/Plants/Pages/Hemp.aspx",
                "mirror_domains": [
                    "illinois.gov/sites/agr/Plants"
                ]
            },
            "ME": {
                "name": "Maine",
                "agency": "Office of Cannabis Policy",
                "main_url": "https://www.maine.gov/dafs/ocp",
                "mirror_domains": [
                    "maine.gov/dafs/ocp"
                ]
            },
            "MD": {
                "name": "Maryland",
                "agency": "Cannabis Control Authority",
                "main_url": "https://mmcc.maryland.gov",
                "mirror_domains": [
                    "mmcc.maryland.gov"
                ]
            },
            "MA": {
                "name": "Massachusetts",
                "agency": "Cannabis Control Commission",
                "main_url": "https://mass-cannabis-control.com",
                "mirror_domains": [
                    "mass-cannabis-control.com"
                ]
            },
            "MI": {
                "name": "Michigan",
                "agency": "Cannabis Regulatory Agency", 
                "main_url": "https://www.michigan.gov/cra",
                "mirror_domains": [
                    "michigan.gov/cra"
                ]
            },
            "MO": {
                "name": "Missouri",
                "agency": "Division of Cannabis Regulation",
                "main_url": "https://health.mo.gov/safety/medical-marijuana",
                "mirror_domains": [
                    "health.mo.gov/safety/medical-marijuana"
                ]
            },
            "MT": {
                "name": "Montana",
                "agency": "Cannabis Control Division",
                "main_url": "https://mtrevenue.gov/cannabis",
                "mirror_domains": [
                    "mtrevenue.gov/cannabis"
                ]
            },
            "NV": {
                "name": "Nevada", 
                "agency": "Cannabis Compliance Board",
                "main_url": "https://ccb.nv.gov",
                "mirror_domains": [
                    "ccb.nv.gov"
                ]
            },
            "NJ": {
                "name": "New Jersey",
                "agency": "Cannabis Regulatory Commission",
                "main_url": "https://www.nj.gov/cannabis",
                "mirror_domains": [
                    "nj.gov/cannabis"
                ]
            },
            "NM": {
                "name": "New Mexico",
                "agency": "Regulation and Licensing Department",
                "main_url": "https://www.rld.nm.gov/cannabis-control-division",
                "mirror_domains": [
                    "rld.nm.gov/cannabis-control-division"
                ]
            },
            "NY": {
                "name": "New York", 
                "agency": "Office of Cannabis Management",
                "main_url": "https://cannabis.ny.gov",
                "mirror_domains": [
                    "cannabis.ny.gov"
                ]
            },
            "RI": {
                "name": "Rhode Island",
                "agency": "Department of Business Regulation",
                "main_url": "https://dbr.ri.gov/divisions/commercial-licensing/cannabis",
                "mirror_domains": [
                    "dbr.ri.gov/divisions/commercial-licensing/cannabis"
                ]
            },
            "VT": {
                "name": "Vermont",
                "agency": "Cannabis Control Board", 
                "main_url": "https://ccb.vermont.gov",
                "mirror_domains": [
                    "ccb.vermont.gov"
                ]
            },
            "VA": {
                "name": "Virginia",
                "agency": "Cannabis Control Authority",
                "main_url": "https://www.vacannabiscontrolauthority.com",
                "mirror_domains": [
                    "vacannabiscontrolauthority.com"
                ]
            },
            "FL": {
                "name": "Florida (Medical Only)",
                "agency": "Department of Health",
                "main_url": "https://knowthefactsmmj.com",
                "mirror_domains": [
                    "knowthefactsmmj.com",
                    "flrules.org/gateway/department.asp?id=64"
                ]
            },
            "OH": {
                "name": "Ohio (Medical Only)",
                "agency": "Department of Commerce",
                "main_url": "https://www.com.ohio.gov/divisions/division-of-industrial-compliance-and-labor/bureaus/bureau-of-workers-compensation/medical-marijuana-control-program",
                "mirror_domains": [
                    "com.ohio.gov/divisions/division-of-industrial-compliance-and-labor"
                ]
            },
            "PA": {
                "name": "Pennsylvania (Medical Only)", 
                "agency": "Department of Health",
                "main_url": "https://www.health.pa.gov/topics/programs/Medical%20Marijuana",
                "mirror_domains": [
                    "health.pa.gov/topics/programs/Medical%20Marijuana"
                ]
            }
        }
    
    def create_state_directory(self, state_code: str) -> str:
        """Create directory for state website mirror"""
        state_dir = os.path.join(self.base_dir, state_code)
        os.makedirs(state_dir, exist_ok=True)
        return state_dir
    
    def check_mirror_quality(self, state_dir: str, domain: str) -> dict:
        """Check the quality of a mirrored domain"""
        domain_dir = os.path.join(state_dir, domain.replace('/', '_').replace(':', ''))
        
        if not os.path.exists(domain_dir):
            return {"status": "failed", "files": 0, "size": 0, "has_html": False}
        
        file_count = 0
        total_size = 0
        has_html = False
        
        for root, dirs, files in os.walk(domain_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.exists(file_path):
                    file_count += 1
                    total_size += os.path.getsize(file_path)
                    if file.endswith('.html'):
                        has_html = True
        
        if file_count == 0:
            status = "failed"
        elif file_count < 5:
            status = "partial"
        elif has_html and file_count >= 10:
            status = "good"
        else:
            status = "partial"
            
        return {
            "status": status,
            "files": file_count,
            "size": total_size,
            "has_html": has_html,
            "size_mb": round(total_size / 1024 / 1024, 2)
        }

    def mirror_state_website(self, state_code: str) -> bool:
        """Mirror entire regulatory website for a specific state"""
        if state_code not in self.state_sites:
            logger.error(f"Unknown state code: {state_code}")
            return False
            
        state_info = self.state_sites[state_code]
        state_dir = self.create_state_directory(state_code)
        
        logger.info(f"Mirroring website for {state_info['name']} ({state_code})")
        
        success = True
        domain_results = {}
        for domain in state_info['mirror_domains']:
            try:
                # Create subdirectory for this domain
                domain_dir = os.path.join(state_dir, domain.replace('/', '_').replace(':', ''))
                os.makedirs(domain_dir, exist_ok=True)
                
                # First try a simple connectivity test
                test_cmd = ['curl', '-I', '--connect-timeout', '10', f'https://{domain}']
                test_result = subprocess.run(test_cmd, capture_output=True, text=True)
                
                if test_result.returncode != 0:
                    logger.warning(f"Connectivity test failed for {domain}: {test_result.stderr}")
                    # Try HTTP instead of HTTPS
                    test_cmd = ['curl', '-I', '--connect-timeout', '10', f'http://{domain}']
                    test_result = subprocess.run(test_cmd, capture_output=True, text=True)
                    if test_result.returncode != 0:
                        logger.error(f"Domain {domain} is unreachable")
                        quality = self.check_mirror_quality(state_dir, domain)
                        domain_results[domain] = quality
                        continue
                
                # Try multiple approaches for downloading
                success = False
                
                # Approach 1: Use wget with better headers
                cmd = [
                    'wget',
                    '--mirror',
                    '--convert-links',
                    '--adjust-extension',
                    '--page-requisites',
                    '--no-parent',
                    '--recursive',
                    '--level=2',
                    '--timestamping',
                    '--wait=3',
                    '--random-wait',
                    '--timeout=45',
                    '--tries=5',
                    '--reject=mp4,avi,mov,mp3,wav,zip,exe,dmg,pdf',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    '--no-check-certificate',
                    '--header=Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    '--header=Accept-Language: en-US,en;q=0.5',
                    '--header=Accept-Encoding: gzip, deflate',
                    '--header=Connection: keep-alive',
                    '--header=Upgrade-Insecure-Requests: 1',
                    '--directory-prefix=' + domain_dir,
                    f'https://{domain}'
                ]
                
                logger.info(f"Attempting wget mirror for: https://{domain}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
                
                if result.returncode == 0:
                    success = True
                    logger.info(f"wget succeeded for {domain}")
                else:
                    logger.warning(f"wget failed for {domain}, trying alternative approach")
                    
                    # Approach 2: Use curl for single page downloads
                    try:
                        import requests
                        session = requests.Session()
                        session.headers.update({
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1'
                        })
                        
                        # Download main page
                        response = session.get(f'https://{domain}', timeout=30, verify=False)
                        if response.status_code == 200:
                            main_file = os.path.join(domain_dir, 'index.html')
                            os.makedirs(os.path.dirname(main_file), exist_ok=True)
                            with open(main_file, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            success = True
                            logger.info(f"Successfully downloaded main page for {domain}")
                        else:
                            logger.warning(f"Failed to download main page for {domain}: {response.status_code}")
                    except Exception as e:
                        logger.warning(f"Python requests also failed for {domain}: {e}")
                        
                        # Approach 3: Use curl as fallback
                        curl_cmd = [
                            'curl',
                            '-L',  # Follow redirects
                            '-o', os.path.join(domain_dir, 'index.html'),
                            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            '--header', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            '--header', 'Accept-Language: en-US,en;q=0.5',
                            '--connect-timeout', '30',
                            '--max-time', '60',
                            '--retry', '3',
                            '--insecure',
                            f'https://{domain}'
                        ]
                        
                        curl_result = subprocess.run(curl_cmd, capture_output=True, text=True)
                        if curl_result.returncode == 0:
                            success = True
                            logger.info(f"curl succeeded for {domain}")
                        else:
                            logger.error(f"All download methods failed for {domain}")
                
                cmd = []  # Reset for logging
                
                # Check mirror quality regardless of return code
                quality = self.check_mirror_quality(state_dir, domain)
                domain_results[domain] = quality
                
                if success and quality['files'] > 0:
                    logger.info(f"Successfully mirrored: {domain} ({quality['files']} files, {quality['size_mb']}MB)")
                else:
                    logger.warning(f"Mirror failed or incomplete for {domain}: {quality['files']} files")
                    
            except subprocess.TimeoutExpired:
                logger.warning(f"Mirror timeout for {domain} - continuing with partial download")
                quality = self.check_mirror_quality(state_dir, domain)
                domain_results[domain] = quality
            except Exception as e:
                logger.error(f"Error mirroring {domain}: {str(e)}")
                quality = self.check_mirror_quality(state_dir, domain)
                domain_results[domain] = quality
                success = False
        
        # Determine overall success based on domain quality
        overall_success = any(result['status'] in ['good', 'partial'] for result in domain_results.values())
        
        # Create metadata file
        metadata = {
            "state": state_code,
            "name": state_info['name'],
            "agency": state_info['agency'],
            "main_url": state_info['main_url'],
            "mirrored_domains": state_info['mirror_domains'],
            "domain_results": domain_results,
            "last_updated": datetime.now().isoformat(),
            "mirror_success": overall_success,
            "total_files": sum(r['files'] for r in domain_results.values()),
            "total_size_mb": sum(r['size_mb'] for r in domain_results.values())
        }
        
        metadata_path = os.path.join(state_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return success
    
    def mirror_all_websites(self) -> Dict[str, bool]:
        """Mirror regulatory websites for all states"""
        logger.info("Starting website mirroring for all state regulations")
        
        # Create base directory
        os.makedirs(self.base_dir, exist_ok=True)
        
        results = {}
        for state_code in self.state_sites.keys():
            results[state_code] = self.mirror_state_website(state_code)
            
        # Create summary report
        summary = {
            "mirror_date": datetime.now().isoformat(),
            "total_states": len(self.state_sites),
            "successful_mirrors": sum(results.values()),
            "failed_mirrors": len(self.state_sites) - sum(results.values()),
            "results": results
        }
        
        summary_path = os.path.join(self.base_dir, 'mirror_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        logger.info(f"Mirroring complete. Success: {summary['successful_mirrors']}/{summary['total_states']}")
        return results

def main():
    """Main function to run the website mirror"""
    mirror = RegulationMirror()
    results = mirror.mirror_all_websites()
    
    # Print summary
    successful = sum(results.values())
    total = len(results)
    print(f"\n🌐 Website Mirror Summary:")
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful < total:
        print("\n⚠️  Failed mirrors:")
        for state, success in results.items():
            if not success:
                print(f"   - {state}")
    
    print(f"\n📁 Complete website mirrors stored in 'regulations/' directory")
    print(f"📊 Check 'regulations/mirror_summary.json' for detailed results")

if __name__ == "__main__":
    main()
