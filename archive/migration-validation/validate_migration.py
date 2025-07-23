#!/usr/bin/env python3
"""
Validation script to test the new SRV1 and JSON3 parsers with existing files.
"""

import sys
import os
sys.path.append('.')

# Import the new parser functions
try:
    from enhanced_server import parse_srv1_content, parse_json3_content, parse_vtt_content_legacy
    print("✅ Successfully imported parser functions from enhanced_server")
except ImportError as e:
    print(f"❌ Import error from enhanced_server: {e}")
    sys.exit(1)

def test_parsers():
    """Test the parsers with existing sample files."""
    base_name = "Fei-Fei Li： Spatial Intelligence is the Next Frontier in AI [_PioN-CpOP0].en"
    
    # Test files
    vtt_file = f"{base_name}.vtt"
    srv1_file = f"{base_name}.srv1"
    json3_file = f"{base_name}.json3"
    
    results = {}
    
    # Test VTT (legacy)
    if os.path.exists(vtt_file):
        try:
            vtt_lines = parse_vtt_content_legacy(vtt_file)
            results['vtt'] = {
                'success': True,
                'line_count': len(vtt_lines),
                'sample_lines': vtt_lines[:3]
            }
            print(f"✅ VTT parser: {len(vtt_lines)} lines")
        except Exception as e:
            results['vtt'] = {'success': False, 'error': str(e)}
            print(f"❌ VTT parser failed: {e}")
    else:
        print(f"⚠️  VTT file not found: {vtt_file}")
    
    # Test SRV1
    if os.path.exists(srv1_file):
        try:
            srv1_lines = parse_srv1_content(srv1_file)
            results['srv1'] = {
                'success': True,
                'line_count': len(srv1_lines),
                'sample_lines': srv1_lines[:3]
            }
            print(f"✅ SRV1 parser: {len(srv1_lines)} lines")
        except Exception as e:
            results['srv1'] = {'success': False, 'error': str(e)}
            print(f"❌ SRV1 parser failed: {e}")
    else:
        print(f"⚠️  SRV1 file not found: {srv1_file}")
    
    # Test JSON3
    if os.path.exists(json3_file):
        try:
            json3_lines = parse_json3_content(json3_file)
            results['json3'] = {
                'success': True,
                'line_count': len(json3_lines),
                'sample_lines': json3_lines[:3]
            }
            print(f"✅ JSON3 parser: {len(json3_lines)} lines")
        except Exception as e:
            results['json3'] = {'success': False, 'error': str(e)}
            print(f"❌ JSON3 parser failed: {e}")
    else:
        print(f"⚠️  JSON3 file not found: {json3_file}")
    
    # Comparison
    print("\n" + "=" * 50)
    print("PARSER VALIDATION RESULTS")
    print("=" * 50)
    
    for format_name, result in results.items():
        if result['success']:
            print(f"{format_name.upper():5}: {result['line_count']} lines")
            print(f"      Sample: {result['sample_lines'][0][:60]}..." if result['sample_lines'] else "      No samples")
        else:
            print(f"{format_name.upper():5}: FAILED - {result['error']}")
    
    # Success check
    successful_parsers = [k for k, v in results.items() if v['success']]
    if len(successful_parsers) >= 2:
        print(f"\n✅ Migration validation successful! {len(successful_parsers)} parsers working.")
        return True
    else:
        print(f"\n❌ Migration validation failed! Only {len(successful_parsers)} parsers working.")
        return False

if __name__ == "__main__":
    success = test_parsers()
    sys.exit(0 if success else 1)
