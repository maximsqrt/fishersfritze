// #include <opencv2/opencv.hpp>
// #include <iostream>

// cv::Point findLure(const cv::Mat& screenImage, const cv::Mat& lureTemplate) {
//     // Check if images are loaded
//     if (screenImage.empty() || lureTemplate.empty()) {
//         std::cerr << "Error: Screen image or lure template is not available." << std::endl;
//         return cv::Point(-1, -1);  // Return invalid point
//     }

//     // Result matrix to store the result of template matching
//     cv::Mat result;

//     // Perform template matching (using normalized correlation coefficient)
//     cv::matchTemplate(screenImage, lureTemplate, result, cv::TM_CCOEFF_NORMED);

//     // Find the global minimum and maximum in the result matrix
//     double minVal, maxVal;
//     cv::Point minLoc, maxLoc;
//     cv::minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc);

//     // Threshold to check if the lure is detected
//     double threshold = 0.6;
//     if (maxVal < threshold) {
//         std::cerr << "Lure not found: correlation value below threshold." << std::endl;
//         return cv::Point(-1, -1);  // Return invalid point if lure not found
//     }

//     // Get the top-left corner of the match and calculate the center of the matched region
//     cv::Point topLeft = maxLoc;
//     int width = lureTemplate.cols;
//     int height = lureTemplate.rows;
//     cv::Point centerLoc(topLeft.x + width / 2, topLeft.y + height / 2);

//     std::cout << "Lure found at position: (" << centerLoc.x << ", " << centerLoc.y << ")" << std::endl;

//     // Return the center location of the matched region
//     return centerLoc;
// }

// int main() {
//     // Load the screen image (replace with actual path)
//     cv::Mat screenImage = cv::imread("path_to_screen_image.png");

//     // Load the lure template image (replace with actual path)
//     cv::Mat lureTemplate = cv::imread("path_to_lure_template.png");

//     // Call the findLure function
//     cv::Point lurePosition = findLure(screenImage, lureTemplate);

//     if (lurePosition.x != -1 && lurePosition.y != -1) {
//         std::cout << "Lure detected at: (" << lurePosition.x << ", " << lurePosition.y << ")" << std::endl;
//     } else {
//         std::cerr << "Lure not detected." << std::endl;
//     }

//     return 0;
// }
