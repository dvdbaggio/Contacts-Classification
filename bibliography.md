# Van Der Waals Interactions

Feature: a1_product

Formula: s_a1 * t_a1
Why it works: a1 measures polarity. This feature captures the joint polarity/hydrophobicity.
A large positive product means either both are hydrophobic (- * - = +) or both are hydrophilic (+ * + = +).
When combined with low RSA, a large positive a1_product strongly suggests a VDW interaction between two buried, hydrophobic residues.
When combined with high RSA, it suggests a polar surface interaction, likely HBOND.
Target Contacts: VDW (primary), HBOND. -> [link](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Physical_Properties_of_Matter/Atomic_and_Molecular_Properties/Intermolecular_Forces/Specific_Interactions/Van_Der_Waals_Interactions)

# IONIC interaction

conferma che un legame ionico si forma tra ioni con cariche opposte, il fattore a5 misura proprio le cariche

Feature: a5_product

Formula: s_a5 * t_a5
Why it works: This is the single most important engineered feature for predicting ionic interactions.
IONIC (Salt Bridge): A positively charged residue (K, R have high positive a5) interacts with a negatively charged one (D, E have high negative a5). The product will be a large negative number.
Charge Repulsion: Two like charges interacting (e.g., K-K or D-E) will result in a large positive number. This is a strong negative signal for a stable contact.
Neutral: If one or both residues are neutral (a5 ≈ 0), the product will be near zero.
Target Contacts: IONIC (primary), helps rule out interactions for other types. -> [link](https://www.sciencedirect.com/topics/materials-science/ionic-bonding#:~:text=4.1%20Ionic%20bonds-,An%20ionic%20bond%20is%20a%20bond%20in%20which%20an%20atom,atoms%20with%20sharply%20dissimilar%20electronegativities)

# HBOND interactions

If two residues are both in an α-helix and are 3-4 residues apart in the sequence (t_resi - s_resi is 3 or 4), they are very likely to have an HBOND. -> [link](https://bio.libretexts.org/Bookshelves/Biochemistry/Fundamentals_of_Biochemistry_(Jakubowski_and_Flatt)/01%3A_Unit_I-_Structure_and_Catalysis/04%3A_The_Three-Dimensional_Structure_of_Proteins/4.02%3A_Secondary_Structure_and_Loops)

HBOND (Hydrogen Bond): If the residues are polar (e.g., S, T, N, Q). -> [link](https://www.sciencedirect.com/topics/chemistry/polar-amino-acid#:~:text=Polar%20amino%20acids%20are%20a,tyrosine%2C%20glutamine%2C%20and%20asparagine)