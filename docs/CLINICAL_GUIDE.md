# Clinical User Guide - Cervical Pose Detection System

## Table of Contents

1. [Introduction](#introduction)
2. [Clinical Applications](#clinical-applications)
3. [Setup and Installation](#setup-and-installation)
4. [Exercise Protocols](#exercise-protocols)
5. [Interpretation Guide](#interpretation-guide)
6. [Troubleshooting](#troubleshooting)
7. [Safety Considerations](#safety-considerations)

## Introduction

The Cervical Pose Detection System is a computer vision-based tool designed to assist healthcare professionals in monitoring and assessing cervical exercise performance. This guide provides clinical protocols, interpretation guidelines, and best practices for integrating the system into patient care.

### Intended Users

- Physical Therapists
- Occupational Therapists
- Chiropractors
- Physiatrists
- Exercise Physiologists
- Certified Athletic Trainers

### Clinical Indications

- Cervical spine mobility assessment
- Post-injury rehabilitation monitoring
- Postural exercise compliance
- Range of motion documentation
- Home exercise program guidance

## Clinical Applications

### Assessment Capabilities

#### Range of Motion Evaluation

The system provides objective measurement of:

- **Cervical Flexion**: Forward head movement (normal: 45-50°)
- **Cervical Extension**: Backward head movement (normal: 45-55°)
- **Lateral Flexion**: Side-to-side movement (normal: 40-45° each side)
- **Cervical Rotation**: Head turning (normal: 60-80° each side)
- **Cervical Retraction**: Posterior translation (functional movement)

#### Movement Quality Assessment

- Real-time movement analysis
- Compensation pattern detection
- Symmetry evaluation
- Movement coordination assessment

#### Progress Monitoring

- Session-to-session comparison
- Objective performance metrics
- Compliance tracking
- Functional improvement documentation

### Clinical Workflow Integration

#### Initial Assessment

1. **Patient History**: Document cervical symptoms and limitations
2. **Physical Examination**: Perform standard cervical assessment
3. **Baseline Measurement**: Use system to establish initial ROM values
4. **Treatment Planning**: Integrate findings into rehabilitation plan

#### Treatment Sessions

1. **Progress Evaluation**: Compare current performance to baseline
2. **Real-time Feedback**: Guide patient through exercises
3. **Quality Control**: Ensure proper exercise technique
4. **Documentation**: Record session metrics and observations

#### Discharge Planning

1. **Final Assessment**: Document improvement and remaining limitations
2. **Home Program**: Provide system-guided exercise protocols
3. **Follow-up**: Schedule periodic reassessments

## Setup and Installation

### System Requirements

#### Hardware Requirements

- **Computer**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Processor**: Intel i5 or equivalent (minimum), i7 recommended
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Camera**: USB webcam or built-in camera (720p minimum, 1080p preferred)
- **Storage**: 2GB free space minimum

#### Software Installation

```bash
# Download and install Python 3.8+
# Clone the repository
git clone https://github.com/hmzi67/cervical-posture-detection
cd cervical-pose-detection

# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run main.py
```

### Clinical Environment Setup

#### Optimal Setup Configuration

1. **Camera Position**:

   - Mount at patient's eye level
   - Distance: 4-6 feet from patient
   - Angle: Directly facing patient
   - Stability: Use tripod or stable mount

2. **Lighting Conditions**:

   - Even frontal lighting preferred
   - Avoid backlighting or harsh shadows
   - Natural light or soft LED lighting optimal
   - Avoid fluorescent lighting if possible

3. **Background**:

   - Plain, contrasting background
   - Avoid busy patterns or multiple colors
   - Ensure clear contrast with patient's clothing
   - Remove distracting objects from view

4. **Patient Positioning**:
   - Stable chair with back support
   - Feet flat on floor
   - Arms relaxed at sides
   - Head and shoulders clearly visible to camera

## Exercise Protocols

### Standardized Assessment Protocol

#### Pre-Assessment Checklist

- [ ] Patient consent obtained
- [ ] System calibrated and tested
- [ ] Optimal lighting verified
- [ ] Camera position adjusted
- [ ] Patient positioned correctly
- [ ] Emergency procedures reviewed

#### Assessment Sequence

##### 1. System Calibration (30 seconds)

- Patient maintains neutral head position
- System automatically calibrates baseline measurements
- Verify "Ready" status for all exercises
- Re-calibrate if accuracy concerns arise

##### 2. Range of Motion Assessment (10-15 minutes)

**Cervical Flexion Protocol:**

- Starting position: Neutral cervical alignment
- Movement: Slowly lower chin toward chest
- End position: Maximum comfortable flexion
- Hold: 3-5 seconds at end range
- Return: Slowly return to neutral
- Repetitions: 3-5 times
- Rest: 10-15 seconds between repetitions

**Cervical Extension Protocol:**

- Starting position: Neutral cervical alignment
- Movement: Slowly tilt head backward
- End position: Maximum comfortable extension
- Hold: 3-5 seconds at end range
- Return: Slowly return to neutral
- Repetitions: 3-5 times
- **Safety Note**: Monitor for dizziness or nausea

**Lateral Flexion Protocol:**

- Starting position: Neutral cervical alignment
- Movement: Tilt head to bring ear toward shoulder
- End position: Maximum comfortable side-bending
- Hold: 3-5 seconds at end range
- Return: Slowly return to neutral
- Repetitions: 3-5 times each direction
- **Important**: Keep shoulders level throughout movement

**Cervical Rotation Protocol:**

- Starting position: Neutral cervical alignment
- Movement: Turn head to look over shoulder
- End position: Maximum comfortable rotation
- Hold: 3-5 seconds at end range
- Return: Slowly return to neutral
- Repetitions: 3-5 times each direction
- **Important**: Keep chin level throughout movement

**Chin Tuck Protocol:**

- Starting position: Neutral cervical alignment
- Movement: Pull chin straight back (posterior translation)
- End position: Maximum comfortable retraction
- Hold: 5-10 seconds
- Return: Slowly return to neutral
- Repetitions: 5-10 times
- **Focus**: Maintain level head position

### Therapeutic Exercise Protocols

#### Phase 1: Acute/Early Stage (Days 1-7)

**Goals**: Pain reduction, gentle mobility restoration

**Protocol**:

- Exercise frequency: 2-3 times daily
- Repetitions: 3-5 per direction
- Hold time: 3-5 seconds
- Intensity: Pain-free range only
- Progression: Based on symptom response

**Exercises**:

- Gentle cervical flexion (50% of normal range)
- Mild cervical retraction
- Supported cervical rotation (seated with headrest)

#### Phase 2: Subacute Stage (Days 7-21)

**Goals**: Progressive range of motion, strength building

**Protocol**:

- Exercise frequency: 3-4 times daily
- Repetitions: 5-8 per direction
- Hold time: 5-8 seconds
- Intensity: Mild stretch sensation acceptable
- Progression: Increase range and hold time

**Exercises**:

- Full range cervical flexion/extension
- Progressive lateral flexion
- Active cervical rotation
- Sustained chin tuck exercises

#### Phase 3: Chronic/Return to Function (Week 3+)

**Goals**: Full range restoration, functional movement

**Protocol**:

- Exercise frequency: 2-3 times daily
- Repetitions: 8-12 per direction
- Hold time: 10-15 seconds
- Intensity: Moderate stretch acceptable
- Progression: Add resistance and endurance

**Exercises**:

- Full range multi-directional movements
- Combined movement patterns
- Dynamic cervical stability exercises
- Functional movement integration

## Interpretation Guide

### Understanding System Feedback

#### Confidence Scores

- **90-100%**: Excellent exercise performance, clear movement pattern
- **70-89%**: Good performance, minor technique variations
- **50-69%**: Moderate performance, consider coaching cues
- **30-49%**: Poor performance, technique instruction needed
- **Below 30%**: Inadequate movement, reassess patient understanding

#### Status Indicators

- **✅ DETECTED**: Exercise performed correctly within parameters
- **⏳ CALIBRATING**: System establishing baseline measurements
- **⚡ READY**: System calibrated and ready for exercise
- **○ NOT DETECTED**: Exercise not performed or insufficient movement
- **❌ ERROR**: Technical issue or pose not visible

### Clinical Interpretation

#### Normal Findings

- Confidence scores consistently >70%
- Symmetric movement patterns (left/right)
- Smooth, controlled movement quality
- Progressive improvement over sessions
- No compensatory movement patterns

#### Abnormal Findings

- Asymmetric confidence scores between sides
- Consistently low confidence despite good effort
- Jerky or uncontrolled movement patterns
- Lack of improvement over multiple sessions
- Apparent compensatory strategies

#### Red Flag Indicators

- Inability to perform any movement direction
- Severe asymmetry (>50% difference between sides)
- Worsening performance over time
- Patient reports of neurological symptoms
- Obvious movement avoidance patterns

### Documentation Guidelines

#### Session Documentation Template

```
Date: ___________  Patient: _______________
Session Duration: _______ minutes

Baseline Measurements:
- Cervical Flexion: ____% confidence
- Cervical Extension: ____% confidence
- Lateral Flexion L/R: ____% / ____%
- Cervical Rotation L/R: ____% / ____%
- Chin Tuck: ____% confidence

Exercise Performance:
- Total repetitions completed: _____
- Average confidence score: _____%
- Movement quality: Excellent / Good / Fair / Poor
- Patient tolerance: Excellent / Good / Fair / Poor

Observations:
- Compensatory patterns noted: ___________
- Patient feedback: ___________________
- Pain level (0-10): Before ____ After ____

Plan:
- Continue current protocol: Yes / No
- Modify exercises: ___________________
- Next session date: _________________

Clinician Signature: ___________________
```

## Troubleshooting

### Common Technical Issues

#### Poor Detection Accuracy

**Symptoms**: Low confidence scores despite good movement
**Solutions**:

1. Check lighting conditions - ensure even frontal lighting
2. Verify camera position - eye level, 4-6 feet distance
3. Assess background - use plain, contrasting background
4. Reset calibration - recalibrate with better neutral position
5. Check patient positioning - ensure head/shoulders visible

#### Calibration Failures

**Symptoms**: System stuck in "calibrating" status
**Solutions**:

1. Ensure patient maintains completely still position
2. Verify adequate lighting on face and neck area
3. Check for camera movement or vibration
4. Restart application if persistent issues
5. Adjust camera angle for better landmark visibility

#### Inconsistent Results

**Symptoms**: Highly variable confidence scores
**Solutions**:

1. Coach patient on consistent movement speed
2. Ensure stable seating position
3. Check for loose clothing or hair obstruction
4. Verify camera stability throughout session
5. Consider environmental factors (lighting changes)

### Clinical Troubleshooting

#### Patient Difficulty with System

**Issues**: Patient anxiety about technology, difficulty following instructions
**Solutions**:

1. Provide clear explanation of system purpose and safety
2. Demonstrate exercises before starting assessment
3. Start with familiar movements to build confidence
4. Use encouraging language and positive reinforcement
5. Allow practice time before formal assessment

#### Discrepancy with Manual Assessment

**Issues**: System results don't match clinical observation
**Solutions**:

1. Verify system calibration accuracy
2. Check for camera angle or positioning issues
3. Consider patient's movement quality vs. quantity
4. Document both findings and note discrepancies
5. Use clinical judgment as primary guide

## Safety Considerations

### Patient Safety Protocols

#### Pre-Exercise Screening

- Review contraindications to cervical exercise
- Assess for cervical instability or fracture
- Screen for vertebrobasilar insufficiency
- Evaluate for severe neurological compromise
- Document current pain levels and symptoms

#### Exercise Precautions

1. **Stop immediately if**:

   - Sudden increase in pain
   - Onset of dizziness or nausea
   - Numbness or tingling in arms/hands
   - Visual disturbances
   - Severe muscle spasm

2. **Monitor closely for**:
   - Gradual increase in symptoms
   - Compensatory movement patterns
   - Signs of fatigue
   - Changes in coordination
   - Patient anxiety or distress

#### Emergency Procedures

- Have emergency contact information readily available
- Know location of nearest emergency medical facility
- Keep communication device accessible during sessions
- Document any adverse events immediately
- Follow institutional emergency protocols

### System Safety

#### Data Privacy

- Ensure patient consent for video recording
- Follow HIPAA guidelines for data handling
- Secure storage of session data
- Limit access to authorized personnel only
- Regular deletion of unnecessary data

#### Equipment Safety

- Regular camera and computer maintenance
- Secure mounting of all equipment
- Clear walkways and emergency exits
- Electrical safety compliance
- Regular software updates and security patches

## Quality Assurance

### Regular System Validation

- Weekly calibration checks
- Monthly accuracy verification
- Quarterly system updates
- Annual equipment assessment
- Ongoing staff training

### Clinical Standards

- Standardized assessment protocols
- Regular inter-rater reliability checks
- Continuing education requirements
- Patient outcome tracking
- Quality improvement initiatives

---

**Document Version**: 1.0  
**Last Updated**: August 2025  
**Clinical Review**: Dr. [Name], PT, DPT  
**Technical Review**: [System Administrator]

**Disclaimer**: This system is intended to assist healthcare professionals in assessment and monitoring. It should not replace clinical judgment or standard care protocols. Always prioritize patient safety and clinical expertise in decision-making.
