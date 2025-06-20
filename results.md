# Multiple (8, for each class) binary classifiers

RUNNARE DA CAPO QUESTE CONFIG PER INCLUDERE LE METRICHE MANCANTI

## Performance w/o features engineering + SMOTE
| Interaction Type | Accuracy | Balanced Accuracy | Feature Importance Plot |
|------------------|----------|-------------------|------------------------|
| HBOND | 0.6426 | 0.6581 | ![](fi_plots/no_fe_smote/1.png) |
| VDW | 0.5178 | 0.5373 | ![](fi_plots/no_fe_smote/2.png) |
| PIPISTACK | 0.9791 | 0.9874 | ![](fi_plots/no_fe_smote/3.png) |
| IONIC | 0.9420 | 0.9615 | ![](fi_plots/no_fe_smote/4.png) |
| PICATION |  0.9784 | 0.9594 | ![](fi_plots/no_fe_smote/5.png) |
| SSBOND | 0.9990 | 0.9472 | ![](fi_plots/no_fe_smote/6.png) |
| PIHBOND | 0.9666 | 0.8200 | ![](fi_plots/no_fe_smote/7.png) |
| Unclassified | 0.7320 | 0.7106 | ![](fi_plots/no_fe_smote/8.png) |


## Performance with features engineering + SMOTE

### `a5` product

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

With `scale_pos_weight` parameter + fixed SMOTE only over training split

| Interaction Type | Accuracy | Balanced Accuracy | Feature Importance Plot |
|------------------|----------|-------------------|------------------------|
| HBOND | 0.6424 | 0.6582 | ![](fi_plots/fe_smote/a5_product/bal1_class_0.png) |
| VDW | 0.5206 | 0.5366 | ![](fi_plots/fe_smote/a5_product/bal1_class_1.png) |
| PIPISTACK | 0.9791 | 0.9873 | ![](fi_plots/fe_smote/a5_product/bal1_class_2.png) |
| IONIC | 0.9421 | 0.9621 | ![](fi_plots/fe_smote/a5_product/bal1_class_3.png) |
| PICATION | 0.9814 | 0.9211 | ![](fi_plots/fe_smote/a5_product/bal1_class_4.png) |
| SSBOND | 0.9990 | 0.9614 | ![](fi_plots/fe_smote/a5_product/bal1_class_5.png) |
| PIHBOND | 0.9694 | 0.7977 | ![](fi_plots/fe_smote/a5_product/bal1_class_6.png) |
| Unclassified | 0.7335 | 0.7123 | ![](fi_plots/fe_smote/a5_product/bal1_class_7.png) |

## Engineered all the features

For each feature (not distinguished between source and target) it was compute 4 ways to combine the features:
- sum
- absolute difference
- product
- average

| Interaction Type | Accuracy | Balanced Accuracy | Feature Importance Plot |
|------------------|----------|-------------------|------------------------|
| HBOND | 0.6422 | 0.6573 | ![](fi_plots/ova/fe_smote/all_features/cm_0.png) |
| VDW | 0.5208 | 0.5361 | ![](fi_plots/fe_smote/all_features/class1.png) |
| PIPISTACK | 0.9791 | 0.9872 | ![](fi_plots/fe_smote/all_features/class2.png) |
| IONIC | 0.9421 | 0.9619 | ![](fi_plots/fe_smote/all_features/class3.png) |
| PICATION | 0.9788 | 0.9560 | ![](fi_plots/fe_smote/all_features/class4.png) |
| SSBOND | 0.9991 | 0.9734 | ![](fi_plots/fe_smote/all_features/class5.png) |
| PIHBOND | 0.9838 | 0.7574 | ![](fi_plots/fe_smote/all_features/class6.png) |
| Unclassified | 0.7396 | 0.7170 | ![](fi_plots/fe_smote/all_features/class7.png) |

| Class | Accuracy | Balanced Accuracy | AUC-ROC | Matthews Correlation | Average Precision | Feature Importance | Confusion Matrix |
|-------|----------|-------------------|---------|---------------------|-------------------|-------------------|------------------|
| 0 | 0.6439 | 0.6605 | 0.7206 | 0.3074 | 0.5565 | ![](fi_plots/ova/fe_smote/all_features/fi_0.png) | ![](fi_plots/ova/fe_smote/all_features/cm_0.png) |
| 1 | 0.5162 | 0.5382 | 0.5549 | 0.0660 | 0.2833 | ![](fi_plots/ova/fe_smote/all_features/fi_1.png) | ![](fi_plots/ova/fe_smote/all_features/cm_1.png) |
| 2 | 0.9790 | 0.9885 | 0.9910 | 0.6096 | 0.4463 | ![](fi_plots/ova/fe_smote/all_features/fi_2.png) | ![](fi_plots/ova/fe_smote/all_features/cm_2.png) |
| 3 | 0.9415 | 0.9640 | 0.9775 | 0.3944 | 0.2393 | ![](fi_plots/ova/fe_smote/all_features/fi_3.png) | ![](fi_plots/ova/fe_smote/all_features/cm_3.png) |
| 4 | 0.9764 | 0.9708 | 0.9914 | 0.3210 | 0.1835 | ![](fi_plots/ova/fe_smote/all_features/fi_4.png) | ![](fi_plots/ova/fe_smote/all_features/cm_3.png) |
| 5 | 0.9990 | 0.9876 | 0.9995 | 0.6374 | 0.4226 | ![](fi_plots/ova/fe_smote/all_features/fi_5.png) | ![](fi_plots/ova/fe_smote/all_features/cm_5.png) |
| 6 | 0.9373 | 0.9002 | 0.9525 | 0.0808 | 0.0174 | ![](fi_plots/ova/fe_smote/all_features/fi_6.png) | ![](fi_plots/ova/fe_smote/all_features/cm_6.png) |
| 7 | 0.7339 | 0.7183 | 0.7953 | 0.4329 | 0.6769 | ![](fi_plots/ova/fe_smote/all_features/fi_7.png) | ![](fi_plots/ova/fe_smote/all_features/cm_7.png) |

### features selection

| Class | Accuracy | Balanced Accuracy | AUC-ROC | Matthews Correlation | Average Precision | Feature Importance | Confusion Matrix |
|-------|----------|-------------------|---------|---------------------|-------------------|-------------------|------------------|
| 0 | 0.6139 | 0.6197 | 0.6685 | 0.2293 | 0.5117 | ![](fi_plots/ova/fe_smote/all_features/fi_0.png) | ![](fi_plots/ova/fe_smote/all_features/cm_0.png) |
| 1 | 0.5015 | 0.5279 | 0.5396 | 0.0483 | 0.2713 | ![](fi_plots/ova/fe_smote/all_features/fi_1.png) | ![](fi_plots/ova/fe_smote/all_features/cm_1.png) |
| 2 | 0.9789 | 0.9886 | 0.9909 | 0.6090 | 0.4458 | ![](fi_plots/ova/fe_smote/all_features/fi_2.png) | ![](fi_plots/ova/fe_smote/all_features/cm_2.png) |
| 3 | 0.9428 | 0.9600 | 0.9767 | 0.3950 | 0.2278 | ![](fi_plots/ova/fe_smote/all_features/fi_3.png) | ![](fi_plots/ova/fe_smote/all_features/cm_3.png) |
| 4 | 0.9753 | 0.9710 | 0.9911 | 0.3145 | 0.1793 | ![](fi_plots/ova/fe_smote/all_features/fi_4.png) | ![](fi_plots/ova/fe_smote/all_features/cm_3.png) |
| 5 | 0.8413 | 0.7124 | 0.8165 | 0.0309 | 0.0141 | ![](fi_plots/ova/fe_smote/all_features/fi_5.png) | ![](fi_plots/ova/fe_smote/all_features/cm_5.png) |
| 6 | 0.9044 | 0.8768 | 0.9351 | 0.0628 | 0.0086 | ![](fi_plots/ova/fe_smote/all_features/fi_6.png) | ![](fi_plots/ova/fe_smote/all_features/cm_6.png) |
| 7 | 0.6788 | 0.6595 | 0.7239 | 0.3160 | 0.5917 | ![](fi_plots/ova/fe_smote/all_features/fi_7.png) | ![](fi_plots/ova/fe_smote/all_features/cm_7.png) |

### Unified models

**Overall Model Performance**

| Metric | Value |
|--------|-------|
| Accuracy | 0.4870 |
| Balanced Accuracy | 0.7029 |
| Matthews Correlation Coefficient | 0.2795 |

**Per-Class Metrics**

| Class | ROC AUC | Average Precision |
|-------|---------|-------------------|
| HBOND | 0.7206 | 0.5565 |
| VDW | 0.5549 | 0.2833 |
| PIPISTACK | 0.9910 | 0.4463 |
| IONIC | 0.9775 | 0.2393 |
| PICATION | 0.9914 | 0.1835 |
| SSBOND | 0.9995 | 0.4226 |
| PIHBOND | 0.9525 | 0.0174 |
| Unclassified | 0.7953 | 0.6769 |
| **Macro-Average** | **0.8728** | **0.3532** |

**Selected features**

**Overall Performance Metrics**

| Metric | Value |
|--------|-------|
| Accuracy | 0.3317 |
| Balanced Accuracy | 0.3141 |
| Matthews Correlation Coefficient | 0.1411 |

**Per-Class Metrics**

| Class | ROC AUC | Average Precision |
|-------|---------|-------------------|
| HBOND | 0.6699 | 0.5180 |
| VDW | 0.5360 | 0.2679 |
| PIPISTACK | 0.8114 | 0.0657 |
| IONIC | 0.7908 | 0.0412 |
| PICATION | 0.7959 | 0.0207 |
| SSBOND | 0.8471 | 0.0420 |
| PIHBOND | 0.7761 | 0.0150 |
| Unclassified | 0.6767 | 0.5402 |
| **Macro-Average** | **0.7380** | **0.1888** |

![](fi_plots/ova/fe_smote/all_features/fe_unified_model.png)

# A single one multi-class classifier

## Engineered all the features

| Metric | Value |
|--------|-------|
| Accuracy | 0.5417 |
| Balanced Accuracy | 0.3386 |
| AUC-ROC | 0.8825 |
| Matthews Correlation | 0.2889 |
| Average Precision | 0.3741 |

![Feature Importance Plot](fi_plots/mcc/fe_smote/fi_mcc.png)
![Confusion Matrix](fi_plots/mcc/fe_smote/cm_mcc.png)

### features selection

===== Performance Metrics =====
                           Value
Metric                          
Accuracy                  0.4920
Balanced Accuracy         0.2098
AUC-ROC                   0.7430
Matthews Correlation      0.2008
Average Precision         0.2317