Q1="\"3191\":{\"_id\":3191,\"Q\":[\"A ball is dropped from a height. The time taken to reach the ground is measured as 2.0 s.  What is the height from which the ball was dropped (assuming,  g = 9.8 m/s²)?\",\"a\",\"b\",\"c\",\"d\"],\"subject\":\"Math\",\"topic\":\"Algebra\",\"subtopic\":\"Determinants\",\"difficulty\":1,\"grade\":11}";
Q2="\"3192\":{\"_id\":3192,\"Q\":[\"In an experiment to determine the focal length of a convex lens using the u-v method, a student obtains the following data: u = 30 cm, v = 60 cm. The errors in u and v are 0.5 cm each. The focal length f is calculated using the lens formula $\\\\frac{1}{f} = \\\\frac{1}{u} + \\\\frac{1}{v}$. What is the error in the focal length?\",\"a\",\"b\",\"c\",\"d\"],\"subject\":\"Math\",\"topic\":\"Algebra\",\"subtopic\":\"Determinants\",\"difficulty\":1,\"grade\":11}";
Q3="\"3193\":{\"_id\":3193,\"Q\":[\"First, calculate f: $\\\\frac{1}{f} = \\\\frac{1}{30} + \\\\frac{1}{60} = \\\\frac{3}{60} = \\\\frac{1}{20}$, so f = 20 cm.  Now, use error propagation. $\\\\frac{\\\\Delta f}{f} = \\\\sqrt{(\\\\frac{\\\\Delta u}{u})^2 + (\\\\frac{\\\\Delta v}{v})^2}$.  $\\\\frac{\\\\Delta f}{20} = \\\\sqrt{(\\\\frac{0.5}{30})^2 + (\\\\frac{0.5}{60})^2} = \\\\sqrt{(\\\\frac{1}{60})^2 + (\\\\frac{1}{120})^2} = \\\\sqrt{\\\\frac{1}{3600} + \\\\frac{1}{14400}} = \\\\sqrt{\\\\frac{4+1}{14400}} = \\\\sqrt{\\\\frac{5}{14400}} = \\\\frac{\\\\sqrt{5}}{120} \\\\approx 0.0416$.  Therefore, $\\\\Delta f = 20 * 0.0416 \\\\approx 0.83$ cm.\",\"a\",\"b\",\"c\",\"d\"],\"subject\":\"Math\",\"topic\":\"Algebra\",\"subtopic\":\"Determinants\",\"difficulty\":1,\"grade\":11}";
Q4="\"3194\":{\"_id\":3194,\"Q\":[\"If $A = \\\\begin{bmatrix} 1 & 2 \\\\\\\\ 3 & 4 \\\\end{bmatrix}$, then the transpose of $A$, denoted as $A^T$, is:\",\"a\",\"b\",\"c\",\"d\"],\"subject\":\"Math\",\"topic\":\"Algebra\",\"subtopic\":\"Determinants\",\"difficulty\":1,\"grade\":11}";
Q5="\"3195\":{\"_id\":3195,\"Q\":[\"content5\",\"a\",\"b\",\"c\",\"d\"],\"subject\":\"Math\",\"topic\":\"Algebra\",\"subtopic\":\"Determinants\",\"difficulty\":1,\"grade\":11}";

data="{"+
        Q1+","+Q2+","+Q3+","+Q4+","+Q5+  
     "}"
sessionStorage.setItem('contentDetails',data);
sessionStorage.setItem('curUser',"username");
contentDetails = JSON.parse(sessionStorage.getItem('contentDetails'));
//alert("Valid json:" + JSON.stringify(contentDetails));
//alert(data)




