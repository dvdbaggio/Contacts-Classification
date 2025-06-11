# Performance with features engineering + SMOTE

## `a5` product

Without `scale_pos_weight` parameter

| Interaction Type | Accuracy | Balanced Accuracy | Feature Importance Plot |
|------------------|----------|-------------------|------------------------|
| HBOND | 0.6766 | 0.5989 | ![](fi_plots/fe_smote/a5_product/class_0.png) |
| VDW | 0.7517 | 0.5001 | ![](fi_plots/fe_smote/a5_product/class_1.png) |
| PIPISTACK | 0.9867 | 0.5560 | ![](fi_plots/fe_smote/a5_product/class_2.png) |
| IONIC | 0.9874 | 0.5035 | ![](fi_plots/fe_smote/a5_product/class_3.png) |
| PICATION | 0.9959 | 0.5527 | ![](fi_plots/fe_smote/a5_product/class_4.png) |
| SSBOND | 0.9990 | 0.7390 | ![](fi_plots/fe_smote/a5_product/class_5.png) |
| PIHBOND | 0.9991 | 0.5278 | ![](fi_plots/fe_smote/a5_product/class_6.png) |
| Unclassified | 0.7354 | 0.6937 | ![](fi_plots/fe_smote/a5_product/class_7.png) |

With `scale_pos_weight` parameter

| Interaction Type | Accuracy | Balanced Accuracy | Feature Importance Plot |
|------------------|----------|-------------------|------------------------|
| HBOND | 0.6410 | 0.6569 | ![](fi_plots/fe_smote/a5_product/bal_class_0.png) |
| VDW | 0.5198 | 0.5349 | ![](fi_plots/fe_smote/a5_product/bal_class_1.png) |
| PIPISTACK | 0.9791 | 0.9870 | ![](fi_plots/fe_smote/a5_product/bal_class_2.png) |
| IONIC | 0.9485 | 0.9353 | ![](fi_plots/fe_smote/a5_product/bal_class_3.png) |
| PICATION | 0.9909 | 0.7615 | ![](fi_plots/fe_smote/a5_product/bal_class_4.png) |
| SSBOND | 0.9991 | 0.9115 | ![](fi_plots/fe_smote/a5_product/bal_class_5.png) |
| PIHBOND | 0.9988 | 0.5611 | ![](fi_plots/fe_smote/a5_product/bal_class_6.png) |
| Unclassified | 0.7324 | 0.7118 | ![](fi_plots/fe_smote/a5_product/bal_class_7.png) |