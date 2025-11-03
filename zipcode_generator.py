"""Generate list of zip codes for analysis."""
from typing import List


class ZipCodeGenerator:
    """
    Generates lists of zip codes for analysis.
    
    Note: For comprehensive analysis, users should provide their own
    list of target zip codes based on their investment geography.
    """
    
    # Sample zip codes from major US metropolitan areas
    MAJOR_METRO_ZIPCODES = {
        'NYC': ['10001', '10002', '10003', '10009', '10010', '10011', '10012', '10013', 
                '10014', '10016', '10017', '10018', '10019', '10021', '10022', '10023',
                '10024', '10025', '10026', '10027', '10028', '10029', '10030', '10031'],
        'LA': ['90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008',
               '90012', '90013', '90014', '90015', '90016', '90017', '90018', '90019',
               '90020', '90021', '90028', '90029', '90031', '90032', '90033', '90034'],
        'Chicago': ['60601', '60602', '60603', '60604', '60605', '60606', '60607', '60608',
                    '60609', '60610', '60611', '60612', '60613', '60614', '60615', '60616',
                    '60617', '60618', '60619', '60620', '60621', '60622', '60623', '60624'],
        'Houston': ['77001', '77002', '77003', '77004', '77005', '77006', '77007', '77008',
                    '77009', '77010', '77011', '77012', '77013', '77014', '77015', '77016',
                    '77017', '77018', '77019', '77020', '77021', '77022', '77023', '77024'],
        'Phoenix': ['85001', '85002', '85003', '85004', '85006', '85007', '85008', '85009',
                    '85012', '85013', '85014', '85015', '85016', '85017', '85018', '85019',
                    '85020', '85021', '85022', '85023', '85024', '85027', '85028', '85029'],
        'Dallas': ['75201', '75202', '75203', '75204', '75205', '75206', '75207', '75208',
                   '75209', '75210', '75211', '75212', '75214', '75215', '75216', '75217',
                   '75218', '75219', '75220', '75223', '75224', '75225', '75226', '75227'],
        'Miami': ['33101', '33109', '33122', '33125', '33126', '33127', '33128', '33129',
                  '33130', '33131', '33132', '33133', '33134', '33135', '33136', '33137',
                  '33138', '33139', '33140', '33141', '33142', '33143', '33144', '33145'],
        'Seattle': ['98101', '98102', '98103', '98104', '98105', '98106', '98107', '98108',
                    '98109', '98112', '98115', '98116', '98117', '98118', '98119', '98121',
                    '98122', '98125', '98126', '98133', '98134', '98136', '98144', '98146'],
        'Boston': ['02108', '02109', '02110', '02111', '02113', '02114', '02115', '02116',
                   '02118', '02119', '02120', '02121', '02122', '02124', '02125', '02126',
                   '02127', '02128', '02129', '02130', '02131', '02132', '02134', '02135'],
        'Austin': ['78701', '78702', '78703', '78704', '78705', '78712', '78717', '78719',
                   '78721', '78722', '78723', '78724', '78725', '78726', '78727', '78728',
                   '78729', '78730', '78731', '78732', '78733', '78734', '78735', '78736'],
    }
    
    @classmethod
    def get_metro_zipcodes(cls, metro: str) -> List[str]:
        """Get zip codes for a specific metro area."""
        return cls.MAJOR_METRO_ZIPCODES.get(metro, [])
    
    @classmethod
    def get_all_major_metros(cls) -> List[str]:
        """Get all available metro areas."""
        return list(cls.MAJOR_METRO_ZIPCODES.keys())
    
    @classmethod
    def get_sample_zipcodes(cls, count: int = 50) -> List[str]:
        """Get a sample of zip codes from various metros."""
        all_zipcodes = []
        for zipcodes in cls.MAJOR_METRO_ZIPCODES.values():
            all_zipcodes.extend(zipcodes)
        
        # Return first 'count' zip codes
        return all_zipcodes[:count]
    
    @classmethod
    def load_zipcodes_from_file(cls, filepath: str) -> List[str]:
        """
        Load zip codes from a text file (one per line).
        
        Args:
            filepath: Path to file containing zip codes
            
        Returns:
            List of zip codes
        """
        try:
            with open(filepath, 'r') as f:
                zipcodes = [line.strip() for line in f if line.strip()]
            return zipcodes
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return []
    
    @classmethod
    def load_zipcodes_from_csv(cls, filepath: str, column: str = 'zipcode') -> List[str]:
        """
        Load zip codes from a CSV file.
        
        Args:
            filepath: Path to CSV file
            column: Name of column containing zip codes
            
        Returns:
            List of zip codes
        """
        try:
            import pandas as pd
            df = pd.read_csv(filepath)
            if column in df.columns:
                return df[column].astype(str).str.zfill(5).tolist()
            else:
                print(f"Column '{column}' not found in CSV")
                return []
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []


