import dubins
import math

def main():
    start_tup = (0, 0, math.pi / 4)
    end_tup = (1, 1, math.pi / 4)
    d_path = dubins.shortest_path(start_tup, end_tup, 3)
    points = d_path.sample_many(0.2)
    print(points)

    # Calculating time
    #print(d_path.path_length())

    #distance_between_points_m = 0.1   # 10cm
    #points, _ = d_path.sample_many(distance_between_points)
    #path.time = (len(points) * distance_between_points) / speed

    ##for i in range(len(points) - 1):
#print(i)
        #print(dist(points[i][0:2], points[i+1][0:2]))






def dist(start_coords, end_coords):
    return math.sqrt(math.pow(start_coords[0] - end_coords[0], 2) + math.pow(start_coords[1] - end_coords[1], 2))

main()