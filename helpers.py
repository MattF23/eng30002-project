def annotate_frame(model, frame, visible_classes=None):
    results = model(frame)
    if visible_classes is not None:
        # --- get filtered classes --- 
        filtered_result = filter_results(model, results[0], visible_classes)
        return filtered_result.plot(), results[0] 
    return results[0].plot(), results[0]  # BGR image and detection result

def filter_results(model, result, visible_classes):
    if not result.boxes or not visible_classes:
        # --- empty result  --- 
        filtered_result = result.new()
        return filtered_result
    
    # --- keep track of indices --- 
    keep_indices = []
    for i, box in enumerate(result.boxes):
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        if class_name in visible_classes:
            keep_indices.append(i)
    
    if not keep_indices:
        # --- empty result --- 
        filtered_result = result.new()
        return filtered_result
    
    # --- add new selected classes --- 
    filtered_result = result.new()
    filtered_result.boxes = result.boxes[keep_indices]
    
    return filtered_result